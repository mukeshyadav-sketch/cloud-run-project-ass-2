#!/bin/bash

echo "Date & Time:" > log.txt
date >> log.txt

echo "" >> log.txt
echo "Disk Usage:" >> log.txt
df -h >> log.txt

echo "" >> log.txt
echo "Logged-in User:" >> log.txt
whoami >> log.txt

if [ ! -d "deploy_app" ]; then
  mkdir deploy_app
fi

mv log.txt deploy_app/
