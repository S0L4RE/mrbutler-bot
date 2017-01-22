MAKEFLAGS += --no-print-directory


.PHONY: help
help: # Show this help screen
	@ack '^[a-zA-Z_-]+:.*?# .*$$' $(MAKEFILE_LIST) |\
	sort |\
	awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


.PHONY: clean
clean: # Clean up test artifacts
	rm -rf ./.cache ./htmlcov .coverage coverage.xml && \
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf && \
	:


.PHONY: prod-push
prod-push: # Push this sucker to prod!
	heroku container:push bot


.PHONY: test
test: # Run the full testing suite
	./scripts/test.sh


.PHONY: test-docker-entry
test-docker-entry: test-flake test-unit # Entry point for the docker test container to run tests


.PHONY: test-flake
test-flake: # Run flake8 against project files
	flake8 -v


.PHONY: test-unit
test-unit: # Run only unit tests
	PYTHONPATH="./bot/" \
	pytest \
	--cov bot \
	--cov-report html \
	--cov-report term \
	--cov-report xml \
	./tests/unit \
	&& :
