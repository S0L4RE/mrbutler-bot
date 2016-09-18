FROM alpine:3.4

RUN apk add --no-cache \
    python3-dev \
    && python3 -m ensurepip

ENV MRB_ROOT /app
WORKDIR ${MRB_ROOT}

RUN pip3 install --upgrade pip

ADD requirements.txt ${MRB_ROOT}
RUN pip3 install -r ${MRB_ROOT}/requirements.txt

ARG PORT
ENV PORT ${PORT}

ARG MRB_DJANGO_SECRET_KEY
ENV MRB_DJANGO_SECRET_KEY {$MRB_DJANGO_SECRET_KEY}

ADD mrbweb/ ${MRB_ROOT}/mrbweb/
WORKDIR ${MRB_ROOT}/mrbweb/

CMD ["gunicorn", "-b 0.0.0.0:8000", "mrbweb.wsgi"]
