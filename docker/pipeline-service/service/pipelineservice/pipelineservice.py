import os

import hvac
from flask import Flask, jsonify, request

from pipelineservice.pipeline_builder import PipelineBuilder
from pipelineservice.pipeline_command import PipelineCommand

app = Flask(__name__)

token = os.environ['TOKEN']
vault_client = hvac.Client(url='https://vault:8200', token=token, verify="/etc/vault/certificates/vault.pem")


@app.route('/pipelines/', methods=['POST'])
def post_pipelines():
    json = request.get_json()
    cmd = to_command(json)
    if cmd is None:
        return jsonify({
            "error": "Invalid command"
        }), 400
    else:
        try:
            PipelineBuilder(vault_client, "gocd-server:8153").build_pipeline(cmd.app_name, cmd.repo, cmd.team_name)
        except Exception as e:
            app.logger.error("Failed with exception " + str(e))
            return jsonify({
                "error": "Command failed"
            }), 500

        return jsonify({
            "result": "Created"
        })


def to_command(json):
    if json is not None:
        try:
            return PipelineCommand(json['appName'], json['repo'], json["teamName"])
        except KeyError as ke:
            app.logger.error("Parsing invalid command: " + str(ke))
    return None
