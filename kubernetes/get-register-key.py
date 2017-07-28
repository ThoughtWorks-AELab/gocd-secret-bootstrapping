#!/usr/bin/python

import subprocess
import xml.etree.ElementTree as ET

def get_register_key(instance_name):
    contents = subprocess.check_output(["kubectl", "exec", "-it", instance_name, "--", "cat", "/go-working-dir/config/cruise-config.xml"])
    doc = ET.fromstring(contents)
    server_element = doc.find('server')
    if server_element != None:
        key = server_element.attrib['agentAutoRegisterKey']
        return key
    return None

def get_pod_name():
    return subprocess.check_output(["kubectl", "get", "pods", "-l", "app=gocd-server", "-o=jsonpath={.items[0] .metadata .name}"])

print (get_register_key(get_pod_name()))