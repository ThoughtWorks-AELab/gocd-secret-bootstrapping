import json
import urllib.request

from gomatic import *
from gomatic.gocd.artifacts import Artifact


class PipelineBuilder:
    def __init__(self, vault_client, go_host):
        self.vault_client = vault_client
        self.go_host = go_host
        self.go_configurator = GoCdConfigurator(HostRestClient(go_host))

    def build_pipeline(self, app_name, git_repo, team_name):
        pipeline_name = app_name + "-pipeline"
        self.build_policy(pipeline_name)
        self.create_go_pipeline(app_name, pipeline_name, git_repo, team_name)

    def build_policy(self, pipeline_name):
        policy = f"""
        path "secret/app/pipeline/{pipeline_name}/*" {{
            capabilities = ["read"]
        }}
        """

        self.vault_client.set_policy(f"{pipeline_name}-policy", policy)

    def setup_app_role(self, pipeline_name):
        # Enable the app role
        self.vault_client.write(f'auth/approle/role/{pipeline_name}', policies=f"{pipeline_name}-policy")

        # Get the app id
        role_id = self.vault_client.read(f'auth/approle/role/{pipeline_name}/role-id')['data']['role_id']

        # Get the secret
        secret_id = self.vault_client.write(f'auth/approle/role/{pipeline_name}/secret-id')['data']['secret_id']

        return {"role_id": role_id, "secret_id": secret_id}

    def create_go_pipeline(self, app_name, pipeline_name, git_repo, team_name):
        pipeline = self.go_configurator \
            .ensure_pipeline_group(team_name) \
            .ensure_replacement_of_pipeline(app_name) \
            .set_git_url(git_repo)

        build_stage = pipeline.ensure_stage("build")
        build_stage.ensure_job("init")
        build_job = build_stage.ensure_job("build")
        build_job.add_task(ExecTask(['./gradlew', 'assemble']))
        build_job.ensure_artifacts({Artifact.get_build_artifact(f"build/libs/{app_name}*.jar")})

        build_image_stage = pipeline.ensure_stage("build_image")
        build_docker_image_job = build_image_stage.ensure_job("build_docker_image")
        build_docker_image_job.add_task(ExecTask(['make', 'push']))

        approle = self.setup_app_role(pipeline_name)
        build_docker_image_job.ensure_encrypted_environment_variables({
            "VAULT_SECRET_ID": self.encrypt(approle['secret_id'])
        })

        build_docker_image_job.ensure_environment_variables({
            "VAULT_ROLE_ID": approle['role_id']
        })

        # This should actually be committed to a git repo, rather than go directly to go
        self.go_configurator.save_updated_config()

    def encrypt(self, value):
        data = json.dumps({
            "value": value
        }).encode('ascii')

        request = urllib.request.Request(f"http://{self.go_host}/go/api/admin/encrypt", data=data,
                                         headers={'Accept': 'application/vnd.go.cd.v1+json',
                                                  "Content-Type": "application/json"})
        response = urllib.request.urlopen(request)
        payload = json.loads(response.read())
        secret = payload['encrypted_value']
        return secret
