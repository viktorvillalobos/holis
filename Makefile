.DEFAULT_GOAL := help

.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)


.PHONY: up
# read AWS credentials and export them to env vars, docker-compose picks them up
up: ## run the project
ifeq (,$(wildcard ./custom-docker-services.yml))
	@echo "Running default backend project..."
	@docker-compose -f local.yml up -d postgres mailhog redis testdb celeryworker celerybeat flower node || true
	@docker-compose -f local.yml run --name django --service-ports --rm django || true
else
	@echo "Running custom backend project..."
	@docker-compose -f docker-compose.yml -f custom-docker-services.yml run --service-ports --rm backend || true
endif


.PHONY: stop
stop: ## stop Docker containers without removing them
	@docker-compose -f local.yml stop

.PHONY: down
down: ## stop and remove Docker containers
	@docker-compose -f local.yml down --remove-orphans

.PHONY: reset
reset: ## update Docker images and reset local databases
reset:
	@docker-compose down --volumes --remove-orphans
	@docker-compose pull

.PHONY: rebuild
rebuild:
	@docker-compose -f local.yml down --volumes --remove-orphans
	@docker-compose -f local.yml build

.PHONY: bash
bash: ## drop you into a running container
	@docker-compose -f local.yml run --rm django

.PHONY: shell_plus 
shell: ## drop you into a running container as root
	@docker-compose -f local.yml run --rm django ./manage.py shell_plus
