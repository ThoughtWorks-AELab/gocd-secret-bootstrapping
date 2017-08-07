# Go CD Secret Bootstrapping with Vault

Demonstrates the process of bootstrapping a GoCD instance with app role. This is a work in progress. In order to be a fully functional reference implementation, it needs some updates:

* TLS certificates for Vault
* Securing Go CD so it isn't open and the pipeline permissions are set correctly
* Cleanup of the bootstrap_pipeline.py to clarify responsibilities
* Better usage instructions
* A little bit better bootstrap automation
    * Better token handling on Vault spin up
    * Plugging the service hosts into the bootstrap script so you don't have to mess with them
    * Auto-register go agents
    
It is also dependent on another repo for demonstrating how the secret is used to push to a container repo.

# Requirements

* [hvac](https://github.com/ianunruh/hvac): python client library for vault
