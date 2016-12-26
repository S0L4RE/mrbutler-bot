FROM alpine:3.4

ARG MRB_ENV
ENV MRB_ENV ${MRB_ENV}
ENV MRB_ROOT /app
WORKDIR ${MRB_ROOT}

RUN apk add --no-cache \
    build-base \
    python3-dev \
    && python3 -m ensurepip \
    && pip3 install --upgrade pip \
    && pip3 install --upgrade setuptools \
    && :

# Common Image Above
# Different Image Settings Below

ARG MRB_DJANGO_SECRET_KEY
ENV MRB_DJANGO_SECRET_KEY ${MRB_DJANGO_SECRET_KEY}
ENV PORT ${PORT}

RUN apk add --no-cache postgresql-dev

ADD web/requirements.txt ${MRB_ROOT}
RUN pip3 install -r ${MRB_ROOT}/requirements.txt

WORKDIR ${MRB_ROOT}/mrbweb/

# Common WEB Image Above
# Different Image Settings Below

ADD web/mrbweb/ ${MRB_ROOT}/mrbweb/

RUN python3 manage.py collectstatic --noinput
CMD gunicorn -b 0.0.0.0:${PORT} core.wsgi
