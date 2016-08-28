FROM ubuntu:16.04

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libffi-dev \
    opus-tools \
    python3 \
    python3-dev \
    python3-pip \
    && rm -rfv /var/lib/apt/lists/*

ENV MRB_ROOT /mrb
ENV PYTHONPATH ${PYTHONPATH}:/usr/bin
WORKDIR ${MRB_ROOT}

RUN pip3 install --upgrade pip
ADD requirements.txt ${MRB_ROOT}
RUN pip3 install -r ${MRB_ROOT}/requirements.txt

ARG MRB_ADMIN_ID
ARG MRB_DISCORD_TOKEN

ENV MRB_ADMIN_ID ${MRB_ADMIN_ID}
ENV MRB_DISCORD_TOKEN ${MRB_DISCORD_TOKEN}

ADD media/ ${MRB_ROOT}/media/
ADD mrb/ ${MRB_ROOT}/mrb/

ADD mrb.py ${MRB_ROOT}

CMD ["/usr/bin/python3", "./mrb.py"]
