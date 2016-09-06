.PHONY: help
help: # Show this help screen
	@ack '^[a-zA-Z_-]+:.*?# .*$$' $(MAKEFILE_LIST) |\
	sort |\
	awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


.PHONY: dev-all
dev-all: dev-build dev-run # Build AND run the dev docker container


.PHONY: dev-build
dev-build: # Build the dev docker container
	docker build \
	--build-arg MRB_ADMIN_ID=${MRB_ADMIN_ID} \
	--build-arg MRB_DISCORD_TOKEN=${MRB_DISCORD_TOKEN} \
	-t dev-bot .


.PHONY: dev-run
dev-run: # Run the dev docker container
	docker run dev-bot


.PHONY: prod-build
prod-build: # Build the production docker containers
	docker build -f docker/Dockerfile-bot -t prod-bot . && \
	docker tag prod-bot registry.heroku.com/mrbutler/bot


.PHONY: prod-push
prod-push: prod-build # Push this sucker to prod!
	docker push registry.heroku.com/mrbutler/bot


.PHONY: test-clean
test-clean: # Clean up test artificats
	rm -rf ./.cache ./tests/.cache/ ./htmlcov .coverage


.PHONY: test-pep8
test-pep8: # Run pep8 against project files
	pep8 --verbose ./mrb/* ./tests/*


.PHONY: test-pylint
test-pylint: # Run pylint against the project
	pylint --rcfile=./.pylintrc --reports=y --output-format=text mrb


.PHONY: test-travis
test-travis: test-pep8 test-pylint test-unit # Run the full Travis CI testing suite


.PHONY: test-unit
test-unit: # Run only unit tests
	py.test --cov mrb --cov-report html ./tests/unit
