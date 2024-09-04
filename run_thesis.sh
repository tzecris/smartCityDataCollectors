#!/bin/bash

install_if_not_installed() {
    if ! dpkg -l | grep -q $1; then
        echo "Installing $1..."
        sudo apt-get update
        sudo apt-get install -y $1
    else
        echo "$1 is already installed."
    fi
}
install_docker_compose() {
    echo "Installing docker-compose..."
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    if ! docker-compose --version > /dev/null 2>&1; then
        echo "Failed to install docker-compose. Exiting."
        exit 1
    fi
    echo "docker-compose installed successfully."
}

docker_version=$(docker --version | grep -oP '\d+\.\d+\.\d+' | head -1)
if [[ $(echo "$docker_version > 20" | bc -l) -eq 1 ]]; then
    echo "Error: Docker version is higher than 20."
    exit 1
else
    echo "Docker version is acceptable: $docker_version"
fi

if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running."
    echo "Please start Docker and ensure it is running to continue."
    exit 1
else
    echo "Docker is running."

    # Install make
    install_if_not_installed make

    # Check if docker-compose exists and is not version 2
    if command -v docker-compose > /dev/null 2>&1; then
        docker_compose_version=$(docker-compose --version | grep -oP '\d+\.\d+' | head -1)
        if [[ $docker_compose_version == 2* ]]; then
            echo "docker-compose version 2.x detected. Installing docker-compose version 1.x..."
            sudo rm /usr/local/bin/docker-compose
            install_docker_compose
        else
            echo "docker-compose version is acceptable: $docker_compose_version"
        fi
    else
        install_docker_compose
    fi
    echo "Starting OpenWhisk using docker-compose..."
    cd docker-compose

    # Get the count of all containers with names containing 'openwhisk'
    container_count=$(docker ps -a --filter "name=openwhisk" --format "{{.ID}}" | wc -l)

    if [ "$container_count" -gt 10 ]; then
        echo "Restart openwhisk containers"
        make run
    else
        echo "Initiate openwhisk containers"
        make quick-start
    fi

    echo "OpenWhisk instance is now available."

    echo "Creating alarm package"
    make create-provider-alarms

fi

