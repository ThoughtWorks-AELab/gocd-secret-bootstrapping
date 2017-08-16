#!/usr/bin/env python3.6
import sys
import subprocess

def run():
    if len(sys.argv) == 1:
        print_help()

    get_command(sys.argv[1])()

def print_help():
    cmd_string = '\n\t\t'.join(map(lambda cmd: f"{cmd} - {commands[cmd][1]}", commands.keys()))
    sys.exit(f'''
        usage: ./go <command>
        
        commands:
                {cmd_string}
    ''')

def install():
    username = input('Docker hub username: ')
    password = input('Docker hub password: ')

    env_file_contents = f'''
export REGISTRY_USERNAME={username}
export REGISTRY_PASSWORD={password}
    '''
    
    env_file = open(".env", "w")
    env_file.write(env_file_contents)
    env_file.close()

def run_cluster():
    subprocess.run("bin/start.sh")

def build_images():
    subprocess.run(['bin/build-images.sh']) 

def destroy_cluster():
    subprocess.run(['make', 'clean'])  

commands = {
    "help": (print_help, "This message"),
    "install": (install, "Set up the environment to run the cluster."),
    "build": (build_images, "Build all the docker images and push them to dockerhub"),
    "run": (run_cluster, "Run the kubernetes cluster with Go CD and Vault"),
    "destroy": (destroy_cluster, "Destroy the cluster and all associated state.")    
}

def get_command(name):
    cmd = commands.get(name)
    if (cmd == None):
        return print_help
    else:
        return cmd[0]

run()