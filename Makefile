#!/usr/bin/env make

FLY_TARGET ?= concourse

PIPELINE_NAME ?= windows-update

DOCKER_IMAGE ?= mcarey/windows-update

.PHONY: *

pipeline:
	fly -t $(FLY_TARGET) sp -p $(PIPELINE_NAME) -c ci/pipeline.yml -l ci/.params.yml

dependencies:
	pip install -r requirements.txt

docker-image:
	docker build -t $(DOCKER_IMAGE) .
