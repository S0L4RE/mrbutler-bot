FROM alpine:3.4

RUN apk add --no-cache \
    build-base \
    postgresql-dev \
    python3-dev \
    && python3 -m ensurepip \
    && pip3 install --upgrade pip \
    && pip3 install --upgrade setuptools \
    && :

ENV MRB_ROOT /app
WORKDIR ${MRB_ROOT}

ADD web/requirements.txt ${MRB_ROOT}
RUN pip3 install -r ${MRB_ROOT}/requirements.txt

WORKDIR ${MRB_ROOT}/mrbweb/

ARG MRB_DJANGO_SECRET_KEY
ENV MRB_DJANGO_SECRET_KEY ${MRB_DJANGO_SECRET_KEY}

# Common Image Above
# Different Image Settings Below

ARG MRB_ENV
ENV MRB_ENV ${MRB_ENV}
ENV PORT ${PORT}

ADD web/mrbweb/ ${MRB_ROOT}/mrbweb/

RUN python3 manage.py collectstatic --noinput
CMD gunicorn -b 0.0.0.0:${PORT} core.wsgi
