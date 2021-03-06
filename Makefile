.PHONY: all build install list push start test


all: list

build:
	docker build -t okibot/processors .

install:
	pip install --upgrade -r requirements.dev.txt

list:
	@grep '^\.PHONY' Makefile | cut -d' ' -f2- | tr ' ' '\n'

push:
	$${CI?"Push is avaiable only on CI/CD server"}
	docker login -e $$DOCKER_EMAIL -u $$DOCKER_USER -p $$DOCKER_PASS
	docker push okibot/processors
	docker-cloud stack inspect processors || docker-cloud stack create --sync -n processors
	docker-cloud stack update --sync processors

start:
	python -m processors.base.cli $(filter-out $@,$(MAKECMDGOALS))

test:
	pylama processors
	py.test

up:
	docker-compose up

%:
	@:
