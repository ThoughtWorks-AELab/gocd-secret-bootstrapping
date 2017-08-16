#!/usr/bin/env python3

import os
import subprocess
import re

initResults = subprocess.check_output(["vault", "init", "-key-shares=1", "-key-threshold=1"]).decode('utf-8')
unsealKey = re.findall('Unseal Key 1: (.*)', initResults)[0]
rootToken =  re.findall('Initial Root Token: (.*)', initResults)[0]

subprocess.check_output(["vault", "unseal", unsealKey])
subprocess.check_output(["vault", "auth", rootToken])
subprocess.check_output(["vault", "auth-enable", "approle"])

print("vault unseal key: " + unsealKey)
print("vault root token: " + rootToken)

