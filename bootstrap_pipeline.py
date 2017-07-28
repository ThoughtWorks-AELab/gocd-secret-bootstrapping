#!/usr/bin/env python
from gomatic import *
from gomatic.gocd.artifacts import Artifact
import os

configurator = GoCdConfigurator(HostRestClient(os.environ['GO_SERVER_HOST']))
pipeline = configurator \
    .ensure_pipeline_group("hello_world_group") \
    .ensure_replacement_of_pipeline("hello_world_app") \
    .set_git_url("https://github.com/danielsomerfield/hello-secret-world.git")

build_stage = pipeline.ensure_stage("build")
build_stage.ensure_job("init")
build_job = build_stage.ensure_job("build")
build_job.add_task(ExecTask(['./gradlew', 'assemble']))
build_job.ensure_artifacts({Artifact.get_build_artifact("build/libs/hello-secret-world.jar")})

build_image_stage = pipeline.ensure_stage("build_image")
build_docker_image_job = build_image_stage.ensure_job("build_docker_image")
build_docker_image_job.add_task(ExecTask(['make']))

##TODO: deploy the container

configurator.save_updated_config()
