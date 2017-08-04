#!/bin/sh
vault init -key-shares=1 -key-threshold=1

echo Please enter the unseal key
read key
vault unseal $key
echo Please enter root token
read token
vault auth $token
vault auth-enable approle