#!/bin/sh
#read -p "Username: " username
read -sp "Password for user postgres: " password

user='postgres'
export PGPASSWORD=$password
echo
