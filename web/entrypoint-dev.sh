#!/usr/bin/env sh

python3 manage.py collectstatic --noinput

if [[ "${MRB_ENV}" != "dev" ]]; then
    echo "MRB_ENV needs to be set to 'dev' for the dev server to run"
    exit 1
else
    echo "'dev' ENV detected"
    exec gunicorn -b 0.0.0.0:${PORT} --reload mrbweb.wsgi
fi
