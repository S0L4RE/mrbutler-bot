.PHONY: help
help: # Show this help screen
	@ack '^[a-zA-Z_-]+:.*?# .*$$' $(MAKEFILE_LIST) |\
	sort |\
	awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


.PHONY: dev
dev: dev-build dev-run # Build AND run the dev docker container


.PHONY: dev-build
dev-build: # Build the dev docker container
	docker build \
	--build-arg MRB_DISCORD_TOKEN=${MRB_DISCORD_TOKEN_DEV} \
	--build-arg MRB_ADMIN_ID=${MRB_ADMIN_ID} \
	-t dev-bot .


.PHONY: dev-run
dev-run: # Run the dev docker container
	docker run dev-bot


.PHONY: prod-push
prod-push: # Push this sucker to prod!
	heroku container:push worker
