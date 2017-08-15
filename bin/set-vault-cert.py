#!/usr/bin/env python

import subprocess
from time import sleep

def wait():
    for i in range (0, 30):
        try:
            subprocess.check_output(["kubectl", "exec", f"{get_pod_name('vault')}", "pwd"])
            return
        except Exception as e:
            error = e
        sleep(1)
    if error:
        raise Exception("Wait timed out. " + str(error))

    
def get_pod_name(app):
    result = subprocess.run(["kubectl", "get", "pods", "-l", f"app={app}", "-o=jsonpath={.items[0] .metadata .name}"], 
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode("utf-8")

def copy_certificate():
    subprocess.check_output(["kubectl", "cp", f"{get_pod_name('vault')}:/etc/vault/certs/vault.pem",
        "/tmp/vault.pem"])
    subprocess.check_output(["kubectl", "cp", "/tmp/vault.pem",
        f"{get_pod_name('gocd-agent')}:/etc/vault/certificates/vault.pem"])
    
wait()
copy_certificate()
