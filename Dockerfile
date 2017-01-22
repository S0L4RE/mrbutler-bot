FROM alpine:3.5

ENV MRB_ROOT /app
WORKDIR ${MRB_ROOT}

RUN apk add --no-cache \
    build-base \
    ca-certificates \
    ffmpeg \
    libffi-dev \
    python3-dev \
    opus-dev \
    && python3 -m ensurepip \
    && pip3 install --upgrade pip \
    && pip3 install --upgrade setuptools \
    && :

ADD requirements.txt ${MRB_ROOT}
RUN pip3 install -r ${MRB_ROOT}/requirements.txt

# COMMON DOCKERFILE ENDS HERE

ADD bot/mrb_core/ ${MRB_ROOT}/mrb_core/
ADD bot/mrb/ ${MRB_ROOT}/mrb/
ADD bot/bot.py ${MRB_ROOT}

CMD python3 bot.py
