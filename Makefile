SHELL=/bin/bash

timestamp := $(shell date +"%Y-%m-%d-%H-%M")
usr := $(shell id -u):$(shell id -g)
devcompose := COMPOSE_FILE=docker-compose.yml:docker-compose.dev.yml

build:
	$(devcompose) docker-compose down
	$(devcompose) docker-compose build
