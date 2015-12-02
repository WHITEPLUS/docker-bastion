#! /usr/bin/env bash

docker-clean() {

  DOCKER_CONTAINERS=`docker ps -a -q`
  DOCKER_IMAGES=$(docker images | awk '/^<none>/ { print $3 }')

  [[ -n $DOCKER_CONTAINERS ]] && docker rm $DOCKER_CONTAINERS
  [[ -n $DOCKER_IMAGES ]] && docker rmi $DOCKER_IMAGES
}

alias docker-clean=docker-clean

alias docker-compose-up-all=docker-compose kill && docker-compose build && docker-compose up -d

alias redis-cli=docker exec -it bastion_cache redis-cli