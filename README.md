# Mr. Butler

[![Build Status](https://travis-ci.org/urda/mr.butler.svg?branch=master)](https://travis-ci.org/urda/mr.butler)
[![codecov](https://codecov.io/gh/urda/mr.butler/branch/master/graph/badge.svg)](https://codecov.io/gh/urda/mr.butler)

## Setting up your environment

You will need:

- `docker`
- `libffi-devel`
- `python3-dev`

Simply perform the following

1. `mkvirtualenv mr.butler -p $(which python3)`
2. Edit `${VIRTUAL_ENV}/bin/postactivate` as following:

```bash
#!/bin/bash
# This hook is sourced after this virtualenv is activated.

export MRB_ADMIN_ID="YOUR DISCORD SNOWFLAKE ID"
export MRB_DISCORD_TOKEN="YOUR DISCORD TOKEN HERE"
```

3. Edit `${VIRTUAL_ENV}/bin/postdeactivate` as follows:

```bash
#!/bin/bash
# This hook is sourced after this virtualenv is deactivated.

unset MRB_ADMIN_ID
unset MRB_DISCORD_TOKEN
```

4. `deactivate` and `workon mr.butler` to load your environment variables

5. `pip install -r requirements.dev.txt`

6. Once `pip` has installed everything correctly, you should run tests to
   confirm everything is working as expected. Running `make test-travis` will
   execute the entire testing suite.

7. You're all done! You can use `docker-compose up -d --build` to start
   the containers.
