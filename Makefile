.PHONY: help
help: # Show this help screen
	@ack '^[a-zA-Z_-]+:.*?# .*$$' $(MAKEFILE_LIST) |\
	sort |\
	awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


.PHONY: prod-build
prod-build: # Build the production docker containers
	docker-compose build bot && \
	docker tag mrbutler_bot registry.heroku.com/mrbutler-bot/bot && \
	:


.PHONY: prod-push
prod-push: prod-build # Push this sucker to prod!
	docker push registry.heroku.com/mrbutler-bot/bot && \
	:


.PHONY: test-clean
test-clean: # Clean up test artifacts
	rm -rf ./.cache ./htmlcov .coverage


.PHONY: test-flake
test-flake: # Run flake8 against project files
	flake8 -v


.PHONY: test
test: test-flake test-unit # Run the full testing suite


.PHONY: test-unit
test-unit: # Run only unit tests
	pytest \
	--cov mrb \
	--cov-report html \
	--cov-report term \
	./tests/unit \
	&& :
