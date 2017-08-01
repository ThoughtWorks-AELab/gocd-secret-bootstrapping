#!/usr/bin/env python
from gomatic import *
from gomatic.gocd.artifacts import Artifact
import os
import urllib.request
import json

def get_encrypted(value):
    data = json.dumps({
        "value":value
    }).encode('ascii')

    request = urllib.request.Request(f"http://{gocd_host}/go/api/admin/encrypt", data=data,
                            headers={'Accept':'application/vnd.go.cd.v1+json', "Content-Type":"application/json"})

    response = urllib.request.urlopen(request)
    payload = json.loads(response.read())
    secret = payload['encrypted_value']
    return secret


gocd_host = os.environ['GO_SERVER_HOST']
registry_username = os.environ['REGISTRY_USERNAME']
encrypted_registry_password = get_encrypted(os.environ['REGISTRY_PASSWORD'])

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
build_docker_image_job.ensure_environment_variables({
    "DOCKER_USERNAME": registry_username
})

build_docker_image_job.ensure_encrypted_environment_variables({
    "DOCKER_PASSWORD": encrypted_registry_password
})

##TODO: deploy the container
# deploy_pod_stage = pipeline.ensure_stage("deploy_pod")
# deploy_pod_job = deploy_pod_stage.ensure_job("deploy_pod")
# deploy_pod_job.add_task(ExecTask(['make', 'deploy']))

configurator.save_updated_config()
