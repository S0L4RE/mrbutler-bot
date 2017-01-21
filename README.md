# Mr. Butler

[![Build Status](https://travis-ci.org/urda/mr.butler.svg?branch=master)](https://travis-ci.org/urda/mr.butler)
[![codecov](https://codecov.io/gh/urda/mr.butler/branch/master/graph/badge.svg)](https://codecov.io/gh/urda/mr.butler)

## Setting up your environment

1. `mkvirtualenv mrbutler-bot -p $(which python3)`

2. Edit `${VIRTUAL_ENV}/bin/postactivate` as following:

    ```bash
    #!/bin/bash
    # This hook is sourced after this virtualenv is activated.

    export MRB_DISCORD_TOKEN="YOUR DISCORD TOKEN HERE"
    export MRB_ENV="dev"
    ```

3. Edit `${VIRTUAL_ENV}/bin/postdeactivate` as follows:

    ```bash
    #!/bin/bash
    # This hook is sourced after this virtualenv is deactivated.

    unset MRB_DISCORD_TOKEN
    unset MRB_ENV
    ```

4. `deactivate` and `workon mrbutler-bot` to load your environment variables

5. `pip install -r requirements-dev.txt` to install dev requirements.

6. Once `pip` has installed everything correctly, you should run tests to
   confirm everything is working as expected. Running `make test-travis` will
   execute the entire testing suite.

7. You're all done! You can use `docker-compose up -d --build` to start
   the containers.

## Running the bot

You can run the bot directly in your `virtualenv` or you can use the container
that is built by `docker-compose`. Both depend on those environment variables
you already setup, so you can switch back and forth with ease.

### Run locally:

1. `workon mrbutler-bot`

2. `python ./bot.py`

3. `Ctrl-C` when done

### Run from `docker`:

1. `workon mrbutler-bot`

2. `docker-compose up --build bot`
  - You can optionally add `-d` before `--build` if you do not mind the
    container detaching from your session and will `docker-compose stop` it
    later on your own.

3. `Ctrl-C` when done
