#!/usr/bin/env make

FLY_TARGET ?= concourse

PIPELINE_NAME ?= windows-update

.PHONY: *

pipeline:
	fly -t $(FLY_TARGET) sp -p $(PIPELINE_NAME) -c ci/pipeline.yml -l ci/.params.yml
