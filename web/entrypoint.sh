#!/usr/bin/env sh

python3 manage.py collectstatic --noinput

if [[ "${MRB_ENV}" == "dev" ]]; then
    echo "'dev' ENV detected"
    exec gunicorn -b 0.0.0.0:${PORT} --reload mrbweb.wsgi
else
    echo "'prod' ENV detected"
    exec gunicorn -b 0.0.0.0:${PORT} mrbweb.wsgi
fi
