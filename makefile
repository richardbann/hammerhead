SHELL=/bin/bash

timestamp := $(shell date +"%Y-%m-%d-%H-%M")
usr := $(shell id -u):$(shell id -g)

.PHONY: init
init:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r .devcontainer/requirements.txt

.PHONY: build
build:
	docker-compose down
	docker-compose build
