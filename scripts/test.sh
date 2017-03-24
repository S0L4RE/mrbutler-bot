#!/usr/bin/env bash

set -euo pipefail

# Change to parent directory
pushd $(git rev-parse --show-toplevel) > /dev/null

make clean

# Run the tests
echo "Running tests INSIDE test docker container..."
docker-compose run --rm --user "${UID}" test sh -c "make test-docker-entry"

# Outta here
popd > /dev/null
