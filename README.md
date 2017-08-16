# Go CD Secret Bootstrapping with Vault

# What this demonstrates

This reference implementation demonstrates the steps to bootstrapping a pipeline that consumes secrets from
Hashicorp Vault, based on the DPS reference architecture for secret management.

# What it does not demonstrate

* A productionalized Vault deploy
* A productionalized Go CD deploy
* Although this does demonstrate the steps for setting up the pipeline, it doesn't current demonstrate how those steps
    are run. Presumably the developer runs a CLI when setting up the project, but the interaction with Go CD happens via
    a privileged service. This allows sensitive operations to happen without credentials needing to be shared with the 
    person running the CLI.

# Notable Components

* Pipeline setup is handled in the gomatic script `bin/boostrap_pipeline.py`. In a production scenario that supports 
    self service, this code would run in the privileged service.


# Setup
* Set up the .env file
* Set up python env

# Building the images
* Start docker

# Running
* Source the .env file
* Source the python env activate
* Start minikube

# Destroying the cluster

Run `make clean` in the root of this project. All running resources will be destroyed.

# Status
In order to be a fully functional reference implementation, it needs some updates:

* Vault stuff
    * Better token handling on Vault spin up
    * Plugging the service hosts into the bootstrap script so you don't have to mess with them
    * Create a policy for the pipeline so it's not using the root token
* Securing Go CD so it isn't open and the pipeline permissions are set correctly
* Cleanup of the bootstrap_pipeline.py to clarify responsibilities
* Better usage instructions

* Eliminate the need for an external docker daemon by using the kube version

It is also dependent on another repo for demonstrating how the secret is used to push to a container repo.

# Requirements
* Docker
* Minikube
* [hvac](https://github.com/ianunruh/hvac): python client library for vault
* virtualenv
