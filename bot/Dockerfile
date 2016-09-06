FROM alpine:3.4

RUN apk add --no-cache \
    build-base \
    ca-certificates \
    ffmpeg \
    libffi-dev \
    opus-dev \
    python3-dev \
    && python3 -m ensurepip

ENV MRB_ROOT /app
ENV PYTHONPATH ${PYTHONPATH}:/usr/bin
WORKDIR ${MRB_ROOT}

RUN pip3 install --upgrade pip
ADD requirements.txt ${MRB_ROOT}
RUN pip3 install -r ${MRB_ROOT}/requirements.txt

ARG MRB_ADMIN_ID
ENV MRB_ADMIN_ID ${MRB_ADMIN_ID}
ARG MRB_DISCORD_TOKEN
ENV MRB_DISCORD_TOKEN ${MRB_DISCORD_TOKEN}

ADD mrb/ ${MRB_ROOT}/mrb/

ADD bot.py ${MRB_ROOT}

CMD ["/usr/bin/python3", "./bot.py"]
