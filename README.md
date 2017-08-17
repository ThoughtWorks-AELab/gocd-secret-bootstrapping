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

# Setup
* Run virtual env to create a python 3.6+ environment and activate it.
    
    `virtualenv -p=python3.6 .pythonenv`

    `. ./.pythonenv/bin/activate`

* Set up the environment
    
    `./go install`

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

# Running the pipeline service

This is a little hacky right now, but will be improved.

* Get the pod for the vault setup task. Depending on spin up time, one may have failed. Choose the one that is "Completed."

    `kubectl get pods --show-all | grep vault-setup`

* Print the logs for that pod. You will see the token printed. **Note that in production, you would not want this data logged**.
    This is for demo purposes only.

    `kubectl logs vault-setup-1234`

* Run `go start_service`. You will be prompted for the token. Enter it and the service is off and running.

# Creating a new pipeline with the service
    
    `./go create_pipeline <app_name> <git_url> <team_name>`

This will create a go project in your pipeline that will do the magic. You should be able to see it by going to the URL
    that was printed out when you started the cluster, or by running `minikube service list | grep gocd-server`

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
* Production-caliber pipeline service. This is really just a slice of the service you would need. A production-ready version would include:
    * command handled async instead of blocking on request
    * re-tries
    * integrated with SSO
    * https
    * spinning up git repo, rather than just requiring it to be pre-setup
    * Pushing policy and initial project to git for pipeline, rather than interacting directly with Vault and Go

# Repos

* Infrastructure repo: 
* Example application repo:

# Roadmap

Path to making this a better reference implementation

* Clean up the process for extracting the root token and pulling a token specifically for the pipeline-service
* Automate the process for setting the registry credentials in vault
* Yank the hard-coded stuff out of the 
* Set permissions on pipeline groups to reflect read-only access to pipelines through UI
* Add support for "template" secrets: as in things that are team or app specific that need to be cofigured
    when application spins up, but shouldn't be public knowledge

