# Go CD Secret Bootstrapping with Vault

## What this demonstrates

This reference implementation demonstrates the steps to bootstrapping a pipeline that consumes secrets from
Hashicorp Vault, based on the DPS reference architecture for secret management. See [what this does not demonstrate](#what-this-does-not-demonstrate) below for aspects of this reference implementation that are non-production ready and will
need additional attention.

## Notable core components

These are the components of the repo that are directly relevant to this reference implementation and should be most 
deeply examined for understanding of how it works.

* Pipeline setup is handled in the gomatic script `bin/boostrap_pipeline.py`. In a production scenario that supports 
    self service, this code would run in the privileged service.
* Cert generation
* CLI service

## Notable extras

A few extra things of note that demonstrate strong platform practices that are broadly relevant.

* ./go file

# Setup
* Run virtual env to create a python 3.6+ environment and activate it.
    
    `virtualenv -p=python3.6 .pythonenv`

    `. ./.pythonenv/bin/activate`

* Start docker
* Start minikube:

    `minikube start`

# Building the images

This only has to be done the first time your run, or if you make a change to one of the docker images.
    
    `./go build`

# Running

    `./go run`

# Destroying the cluster

    `./go destroy`

# Requirements
* docker hub account
* Python 3.6+
* Docker
* Minikube
* virtualenv

# What this does not demonstrate

Aspects of this set up that are out of scope and therefore do not meet production standards. 

* Vault deploy
    * In-memory Vault backend: production deploy should use Consul
    * Automatic Vault unseal, initialization: for convenience the `vault-setup` tasks initializes and unseals Vault. In production
        deploys:
        * Unseal should be manual, possibly require multiple users
        * Initialization should use the -pgp-keys option to protect the integrity of the keys
* A productionalized Go CD deploy
    * All Go endpoints need to be accessible only via TLS 1.2
* Although this does demonstrate the steps for setting up the pipeline, it doesn't current demonstrate how those steps
    are run. Presumably the developer runs a CLI when setting up the project, but the interaction with Go CD happens via
    a privileged service. This allows sensitive operations to happen without credentials needing to be shared with the 
    person running the CLI.

# Roadmap

Path to making this a better reference implementation

* Set permissions on pipeline groups to reflect read-only access to pipelines through UI

# Status
In order to be a fully functional reference implementation, it needs some updates:

* Vault stuff
    * Better token handling on Vault spin up
    * Plugging the service hosts into the bootstrap script so you don't have to mess with them
    * Create a policy for the pipeline so it's not using the root token
* Better usage instructions

It is also dependent on another repo for demonstrating how the secret is used to push to a container repo.
