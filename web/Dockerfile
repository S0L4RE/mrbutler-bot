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

ADD web.py ${MRB_ROOT}

CMD gunicorn -w 4 web:app --bind 0.0.0.0:${PORT}
