.PHONY: help
help: # Show this help screen
	@ack '^[a-zA-Z_-]+:.*?# .*$$' $(MAKEFILE_LIST) |\
	sort |\
	awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


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
test-clean: # Clean up test artifacts
	rm -rf ./.cache ./htmlcov .coverage


.PHONY: test-flake
test-flake: # Run flake8 against project files
	flake8 -v


.PHONY: test-pylint
test-pylint: # Run pylint against the project
	pylint --rcfile=./.pylintrc \
	./bot/mrb \
	./core/mrb_core \
	./web/mrbweb \
	&& :


.PHONY: test
test: test-flake test-pylint test-unit # Run the full testing suite


.PHONY: test-unit
test-unit: # Run only unit tests
	DATABASE_URL="postgres://mrb_test:@localhost:5433/mrb_test" \
	PYTHONPATH="./bot/:./core/:./web/mrbweb" \
	pytest \
	--ds=mrbweb.settings \
	--cov mrb \
	--cov mrb_core \
	--cov django_discord \
	--cov-report html \
	./bot/tests/unit \
	./core/tests/unit \
	./web/mrbweb/ \
	&& :
