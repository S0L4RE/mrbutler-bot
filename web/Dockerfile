FROM alpine:3.4

RUN apk add --no-cache \
    build-base \
    python3-dev \
    && python3 -m ensurepip \
    && pip3 install --upgrade pip \
    && pip3 install --upgrade setuptools \
    && :

ENV MRB_ROOT /app
WORKDIR ${MRB_ROOT}

RUN apk add --no-cache \
    postgresql-dev \
    && :

RUN pip3 install --upgrade ipython

ADD web/requirements.txt ${MRB_ROOT}
RUN pip3 install -r ${MRB_ROOT}/requirements.txt

WORKDIR ${MRB_ROOT}/mrbweb/

ARG MRB_DJANGO_SECRET_KEY
ENV MRB_DJANGO_SECRET_KEY ${MRB_DJANGO_SECRET_KEY}
ENV MRB_ENV ${MRB_ENV}

ENV PORT ${PORT}

ADD web/entrypoint.sh ${MRB_ROOT}
RUN chmod +x ${MRB_ROOT}/entrypoint.sh

ENTRYPOINT ${MRB_ROOT}/entrypoint.sh
CMD ["sh", "-c", "echo ${MRB_ENV}"]
