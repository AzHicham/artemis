.PHONY: compose test stop logs ps
.DEFAULT_GOAL := help

PROJECT_NAME:=artemis

define docker_compose
	COMPOSE_PROJECT_NAME=${PROJECT_NAME} \
	TAG=latest \
	KIRIN_TAG=latest \
	ASGARD_DATA_TAG=france \
	ASGARD_APP_TAG=master \
	docker-compose -f navitia-docker-compose/docker-compose.yml -f navitia-docker-compose/artemis/docker-artemis-instance.yml ${1}
endef

start: ## Deploy Navitia stack and Artemis instances using navitia-docker-compose
	$(call docker_compose, up --detach)

test: build ## Run Artemis tests
	docker run \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-v $$PWD:/usr/src/app \
		--network=${PROJECT_NAME}_default \
		-e ARTEMIS_LOG_LEVEL=DEBUG \
		-e ARTEMIS_USE_ARTEMIS_NG=True \
		-e ARTEMIS_URL_JORMUN='http://${PROJECT_NAME}_jormungandr_1' \
		-e ARTEMIS_URL_TYR='http://${PROJECT_NAME}_tyr_web_1' \
		-e ARTEMIS_DATA_DIR='artemis_data' \
		-e ARTEMIS_REFERENCE_FILE_PATH='artemis_references' \
		-e ARTEMIS_CITIES_DB='postgresql://navitia:navitia@${PROJECT_NAME}_cities_database_1/cities' \
		--rm \
		artemis py.test artemis/tests/bibus_test.py -x --capture=no --showlocals --full-trace

build: ## Build Artemis docker image
	docker build -t artemis .

pull: ## Pull data and container images
	cd artemis_data && git lfs pull # Separate pull as submodule LFS pull is poorly supported
	$(call docker_compose, pull --quiet)

stop: ## Tear down Navitia stack
	$(call docker_compose, down  --volumes --remove-orphans)

clean: ## Remove stopped containers
	$(call docker_compose, rm --force --stop -v)

logsf: ## Display logs and follow
	$(call docker_compose, logs --follow)

logs: ## Display logs
	$(call docker_compose, logs)

ps: ## Display containers information
	$(call docker_compose, ps)

config: ## Display Stack configuration
	$(call docker_compose, config)

##
## Miscellaneous
##
help: ## Print this help message
	@grep -E '^[a-zA-Z_-]+:.*## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

