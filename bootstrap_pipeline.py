#!/usr/bin/env python
from gomatic import *
from gomatic.gocd.artifacts import Artifact
import os
import urllib.request
import json
import hvac

app_name = "hello-secret-world"
pipeline_name = app_name + "-pipeline"
gocd_host = os.environ['GO_SERVER_HOST']
vault_token = os.environ['VAULT_TOKEN']
vault_server = os.environ['VAULT_SERVER']

def setup_policy():
    # TODO: write the policy for the pipeline
    pass

def set_registry_credentials():
    # TODO: set write the credentials for the container registry
    pass


def build_pipeline():
    configurator = GoCdConfigurator(HostRestClient(gocd_host))

    pipeline = configurator \
        .ensure_pipeline_group("hello_world_group") \
        .ensure_replacement_of_pipeline("hello_world_app") \
        .set_git_url("https://github.com/danielsomerfield/hello-secret-world.git")

    build_stage = pipeline.ensure_stage("build")
    build_stage.ensure_job("init")
    build_job = build_stage.ensure_job("build")
    build_job.add_task(ExecTask(['./gradlew', 'assemble']))
    build_job.ensure_artifacts({Artifact.get_build_artifact("build/libs/hello-secret-world*.jar")})

    build_image_stage = pipeline.ensure_stage("build_image")
    build_docker_image_job = build_image_stage.ensure_job("build_docker_image")
    build_docker_image_job.add_task(ExecTask(['make', 'push']))

    approle = setup_app_role()
    build_docker_image_job.ensure_encrypted_environment_variables({
        "VAULT_SECRET_ID": encrypt(approle['secret_id'])
    })

    build_docker_image_job.ensure_environment_variables({
        "VAULT_ROLE_ID": approle['role_id']
    })

    configurator.save_updated_config()

def encrypt(value):
    data = json.dumps({
        "value":value
    }).encode('ascii')

    request = urllib.request.Request(f"http://{gocd_host}/go/api/admin/encrypt", data=data,
                            headers={'Accept':'application/vnd.go.cd.v1+json', "Content-Type":"application/json"})

    response = urllib.request.urlopen(request)
    payload = json.loads(response.read())
    secret = payload['encrypted_value']
    return secret

def setup_app_role():
    client = hvac.Client(url=vault_server, token=vault_token)

    #Enable the app role
    client.write(f'auth/approle/role/{pipeline_name}')

    # #Get the app id
    role_id = client.read(f'auth/approle/role/{pipeline_name}/role-id')['data']['role_id']

    #Get the secret
    secret_id = client.write(f'auth/approle/role/{pipeline_name}/secret-id')['data']['secret_id']
    
    return {"role_id": role_id, "secret_id": secret_id}

# build_pipeline()