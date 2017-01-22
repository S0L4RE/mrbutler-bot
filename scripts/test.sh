#!/usr/bin/env bash

set -euo pipefail

# The absolute path of the chewse project directory
export PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/.."

pushd ${PROJECT_DIR} > /dev/null

make clean

# Run the tests
echo "Running tests INSIDE test docker container..."
docker-compose run --rm --user "${UID}" test sh -c "make test-docker-entry"

# Outta here
popd > /dev/null
