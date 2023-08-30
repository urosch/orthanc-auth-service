#!/bin/bash

# List of subfolders
folders=("keycloak" "nginx")
# Get current directory
parent_dir=$(pwd)

# Loop through each folder and build Docker image
for folder in "${folders[@]}"
do
    echo "Building Docker image for $folder..."
    cd "$parent_dir/$folder" || exit
    docker build -t "urosss/$folder" -f "Dockerfile.orthanc-$folder" .
    echo "Docker image built for $folder."
    echo ""
    cd "$parent_dir" || exit
done
