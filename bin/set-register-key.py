#!/usr/bin/env python

import subprocess
import xml.etree.ElementTree as ET
from time import sleep

def get_register_key(instance_name):
    contents = subprocess.check_output(["kubectl", "exec", "-it", instance_name, "--", "cat", "/go-working-dir/config/cruise-config.xml"])
    doc = ET.fromstring(contents)
    server_element = doc.find('server')
    if server_element != None:
        key = server_element.attrib['agentAutoRegisterKey']
        return key
    return None

def get_pod_name():
    result = subprocess.run(["kubectl", "get", "pods", "-l", "app=gocd-server", "-o=jsonpath={.items[0] .metadata .name}"], 
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout

def register_key():
    error = None
    for i in range (0, 30):
        try:
            return get_register_key(get_pod_name())
        except Exception as e:
            error = e
            pass
        sleep(1)
    if error:
        raise Exception("Failed to get register key: " + str(error))

def run():
    key = register_key()
    result = subprocess.run(["kubectl", "create", "secret", "generic", "go-secrets", f"--from-literal=autoregister-key={key}"], 
            check=True)

run()