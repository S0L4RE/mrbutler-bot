.PHONY: help
help: # Show this help screen
	@ack '^[a-zA-Z_-]+:.*?# .*$$' $(MAKEFILE_LIST) |\
	sort |\
	awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


.PHONY: prod-push
prod-push: # Push this sucker to prod!
	heroku container:push bot


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
	PYTHONPATH="./bot/" \
	pytest \
	--cov bot \
	--cov-report html \
	--cov-report term \
	./tests/unit \
	&& :
