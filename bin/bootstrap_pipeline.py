#!/usr/bin/env python
from gomatic import *
from gomatic.gocd.artifacts import Artifact
import os
import urllib.request
import json
import hvac

def run():
    
    app_name = "hello-secret-world"
    pipeline_name = app_name + "-pipeline"

    setup_policy(
        pipeline_name,
        vault_server = os.environ['VAULT_SERVER'],
        vault_token = os.environ['VAULT_SERVER_TOKEN']
    )

    set_registry_credentials(
        pipeline_name,
        vault_server = os.environ['VAULT_SERVER'],
        vault_token = os.environ['VAULT_SERVER_TOKEN']
    )

    build_pipeline(
        gocd_host = os.environ['GO_SERVER_HOST'],
        pipeline_name = pipeline_name,
        vault_server = os.environ['VAULT_SERVER'],
        vault_token = os.environ['VAULT_SERVER_TOKEN']
    )

def build_pipeline(gocd_host, pipeline_name, vault_server, vault_token):

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

    approle = setup_app_role(pipeline_name, vault_server, vault_token)
    build_docker_image_job.ensure_encrypted_environment_variables({
        "VAULT_SECRET_ID": encrypt(approle['secret_id'], gocd_host)
    })

    build_docker_image_job.ensure_environment_variables({
        "VAULT_ROLE_ID": approle['role_id']
    })

    configurator.save_updated_config()

def encrypt(value, gocd_host):
    data = json.dumps({
        "value":value
    }).encode('ascii')

    request = urllib.request.Request(f"http://{gocd_host}/go/api/admin/encrypt", data=data,
                            headers={'Accept':'application/vnd.go.cd.v1+json', "Content-Type":"application/json"})

    response = urllib.request.urlopen(request)
    payload = json.loads(response.read())
    secret = payload['encrypted_value']
    return secret

def setup_app_role(pipeline_name, vault_server, vault_token):
    client = hvac.Client(url=vault_server, token=vault_token)

    #Enable the app role
    client.write(f'auth/approle/role/{pipeline_name}', policies=f"{pipeline_name}-policy")

    #Get the app id
    role_id = client.read(f'auth/approle/role/{pipeline_name}/role-id')['data']['role_id']

    #Get the secret
    secret_id = client.write(f'auth/approle/role/{pipeline_name}/secret-id')['data']['secret_id']
    
    return {"role_id": role_id, "secret_id": secret_id}

def setup_policy(pipeline_name, vault_server, vault_token):
    # This is just for testing. The real implementation, covered in #645 would indicate
    # that the policy is committed to git, then the pipeline pushes it to vault.

    policy = f"""
path "secret/app/pipeline/{pipeline_name}/*" {{
    capabilities = ["read"]
}}
    """
    
    client = hvac.Client(url=vault_server, token=vault_token) 
    client.set_policy(f"{pipeline_name}-policy", policy) 
    pass

def set_registry_credentials(pipeline_name, vault_server, vault_token):
    client = hvac.Client(url=vault_server, token=vault_token)
    client.write(f'secret/app/pipeline/{pipeline_name}/registry', #TODO: change this convention
        username=os.environ['REGISTRY_USERNAME'], 
        password=os.environ['REGISTRY_PASSWORD'])
        
run()