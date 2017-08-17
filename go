#!/usr/bin/env python3.6
import sys
import subprocess
import urllib.request
import json

def run():
    if len(sys.argv) == 1:
        print_help(sys.argv)

    get_command(sys.argv[1])(sys.argv)

def print_help(args):
    cmd_string = '\n\t\t'.join(map(lambda cmd: f"{cmd} - {commands[cmd][1]}", commands.keys()))
    sys.exit(f'''
        usage: ./go <command>
        
        commands:
                {cmd_string}
    ''')

def install(args):
    username = input('Docker hub username: ')
    password = input('Docker hub password: ')

    env_file_contents = f'''
export REGISTRY_USERNAME={username}
export REGISTRY_PASSWORD={password}
    '''
    
    env_file = open(".env", "w")
    env_file.write(env_file_contents)
    env_file.close()

def run_cluster(args):
    subprocess.run("bin/start.sh")

def build_images(args):
    subprocess.run(['bin/build-images.sh']) 

def destroy_cluster(args):
    subprocess.run(['make', 'clean'])  

def start_pipeline_service(args):
    # prompt for the secret
    token = input('Enter token: ')
    username = input('Enter docker hub username: ')
    password = input('Enter docker hub password: ')

    # set the token as a kube secret
    result = subprocess.run([
        "kubectl", "create", "secret", "generic", "pipelineservice-secrets",
        f"--from-literal=vault-token={token}", f"--from-literal=registry-username={username}",
        f"--from-literal=registry-password={password}"],
        check=True)

    # run the service
    subprocess.run(['bin/start-service.sh']) 

def print_create_pipeline_help():
     sys.exit(f'''
        usage: ./go create_pipeline <app_name> <git_repo> <team_name>
    ''')

def create_pipeline(args):
    service_url = subprocess.run(["minikube", "service", "--url", "pipeline-service"], stdout=subprocess.PIPE).stdout.decode("utf-8").strip()
    if len(args) < 5:
        print_create_pipeline_help()

    app_name = args[2]
    git_repo = args[3]
    team_name = args[4]

    json_cmd = json.dumps({
        "appName":app_name,
        "repo": git_repo,
        "teamName": team_name
    }).encode('ascii')

    request = urllib.request.Request(f"{service_url}/pipelines/", data=json_cmd,
                            headers={'Accept':'application/json', "Content-Type":"application/json"})

    response = urllib.request.urlopen(request)
    print(json.loads(response.read()))

commands = {
    "help": (print_help, "This message"),
    "install": (install, "Set up the environment to run the cluster."),
    "build": (build_images, "Build all the docker images and push them to dockerhub"),
    "run": (run_cluster, "Run the kubernetes cluster with Go CD and Vault"),
    "start_service": (start_pipeline_service, "Start the pipeline service"),
    "create_pipeline": (create_pipeline, "Create a new pipeline"),
    "destroy": (destroy_cluster, "Destroy the cluster and all associated state.")    
}

def get_command(name):
    cmd = commands.get(name)
    if (cmd == None):
        return print_help
    else:
        return cmd[0]

run()