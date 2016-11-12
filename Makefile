.PHONY: help
help: # Show this help screen
	@ack '^[a-zA-Z_-]+:.*?# .*$$' $(MAKEFILE_LIST) |\
	sort |\
	awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


.PHONY: clean
clean: # Clean up test artificats
	rm -rf ./.cache/ ./htmlcov/ .coverage


.PHONY: prod-build
prod-build: # Build the production docker containers
	docker-compose build && \
	docker tag mrbutler_bot registry.heroku.com/mrbutler/bot && \
	docker tag mrbutler_web registry.heroku.com/mrbutler/web && \
	:


.PHONY: prod-pull
prod-pull: # Pull the production docker containers
	docker pull registry.heroku.com/mrbutler/bot && \
	docker pull registry.heroku.com/mrbutler/web && \
	:


.PHONY: prod-push
prod-push: prod-build # Push this sucker to prod!
	docker push registry.heroku.com/mrbutler/bot && \
	docker push registry.heroku.com/mrbutler/web && \
	:


.PHONY: test-clean
test-clean: # Clean up test artificats
	rm -rf ./.cache ./htmlcov .coverage


.PHONY: test-flake8
test-flake8: # Run flake8 against project files
	flake8 -v

.PHONY: test-pep8
test-pep8: # Run pep8 against project files
	pep8 --verbose \
	./bot/*.py \
	./bot/mrb/* \
	./bot/tests/* \
	./core/mrb_core/* \
	./core/tests/* \
	&& :


.PHONY: test-pylint
test-pylint: # Run pylint against the project
	pylint --rcfile=./.pylintrc --reports=y --output-format=text \
	./bot/mrb \
	./core/mrb_core \
	&& :


.PHONY: test-travis
test-travis: test-flake8 test-pep8 test-pylint test-unit # Run the full Travis CI testing suite


.PHONY: test-unit
test-unit: # Run only unit tests
	PYTHONPATH="./bot/:./core/" \
	pytest \
	--cov mrb \
	--cov mrb_core \
	--cov-report html \
	./bot/tests/unit \
	./core/tests/unit \
	&& :
