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
    ca-certificates \
    ffmpeg \
    libffi-dev \
    opus-dev \
    && :

ADD bot/requirements.txt ${MRB_ROOT}
RUN pip3 install -r ${MRB_ROOT}/requirements.txt

ADD core/mrb_core/ ${MRB_ROOT}/mrb_core/
ADD bot/mrb/ ${MRB_ROOT}/mrb/
ADD bot/bot.py ${MRB_ROOT}

ENV MRB_ADMIN_ID ${MRB_ADMIN_ID}
ENV MRB_DISCORD_TOKEN ${MRB_DISCORD_TOKEN}
ENV MRB_ENV ${MRB_ENV}

CMD python3 bot.py
