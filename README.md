# Go CD Secret Bootstrapping with Vault

## What this demonstrates

This reference implementation demonstrates the steps to bootstrapping a pipeline that consumes secrets from
Hashicorp Vault, based on the DPS reference architecture for secret management. See [what this does not demonstrate](#what-this-does-not-demonstrate) below for aspects of this reference implementation that are non-production ready and will
need additional attention. It assumes that there is a service that mediates the approle setup with vault.

## Notable core components

These are the components of the repo that are directly relevant to this reference implementation and should be most 
deeply examined for understanding of how it works.

* Pipeline service - the service that sets up the world. See /docker/pipeline-service/service. Specifically the interaction with Vault and
    Go CD.
* Cert generation - some tricks for creating certificates on demand, particularly with handling hosts. /docker/vault/gencerts.sh
* Example application - example of consuming the secret within the pipeline if you don't have it until the pipeline starts. In this case, 
    the secret is the login for the container registry. Note how the Vault app id and secret id are the core and all secrets are fetched
    based on the identity those represent. https://github.com/ThoughtWorks-AELab/hello-secret-world

## Notable extras

A few extra things of note that demonstrate strong platform practices that are broadly relevant.

* go script - centralized CLI for developers and ops teams
* Vault in kubernetes - doesn't demonstrate anything with the back-end, but it does show how you can do TLS end-to-end
* Setting up Vault with a kubernetes task. The init approach is valid if using the pgp keys. But don't the unseal. It's just
    for demo purposes. It's a bad plan.

# Setup
* Run virtual env to create a python 3.6+ environment and activate it.
    
    `virtualenv -p=python3.6 .pythonenv`

    `. ./.pythonenv/bin/activate`

* Set up the environment. This will just set up you to be able to deploy and pull the images.
    
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
    
To try it with the demo app, run the following command:

    `./go create_pipeline hello-secret-world https://github.com/ThoughtWorks-AELab/hello-secret-world.git hello-team`  

This will make a request to the pipeline service and create a go project in your pipeline that will do the magic. You should be
able to see it by going to the URL that was printed out when you started the cluster, or by running `minikube service list | grep gocd-server`

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
* Production-caliber Pipeline Service. This is really just a slice of the service you would need. A production-ready version would include:
    * Should not just pull the registry creds for env variable. That's just for demo. Normally, every team would have their 
        own and it would presumably be looked up in Vault from a location either controlled by the team, or by the operators,
        depending on the way the operational model is structured. 
    * It should use app-role to authenticate, rather than a hard-coded token
    * command handled async instead of blocking on request
    * re-tries
    * integrated with SSO
    * https
    * spinning up git repo, rather than just requiring it to be pre-setup
    * Pushing policy and initial project to git for pipeline, rather than interacting directly with Vault and Go

# Repos

* Infrastructure repo: https://github.com/ThoughtWorks-AELab/gocd-secret-bootstrapping
* Example application repo: https://github.com/ThoughtWorks-AELab/hello-secret-world

# Roadmap

Path to making this a better reference implementation

* Don't use the root token for the service, but a dedicated token, or even better, an app role
* Clean up the process for extracting the root token and pulling a token specifically for the pipeline-service
* Automate the process for setting the registry credentials in vault
* Pull the hard-coded stuff out of the service, like URLs, and replace with envvars
* Set permissions on pipeline groups to reflect read-only access to pipelines through UI
* Add support for "template" secrets: as in things that are team or app specific that need to be configured
    when application spins up, but shouldn't be public knowledge
* Demonstrate more clearly the push script as a platform-provided resources, so it exists in the code code. It currently resides in the
    application code. 
* Explore whether we can use kubernetes secrets on the filesystem, and then create scripts that are SUIDed to a user that can read them.
    This would prevent users from stealing secrets, even with pipeline code control.