FROM nvidia/cuda:11.4.3-cudnn8-runtime-ubuntu20.04

ENV TZ=Europe/Athens
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    ca-certificates \
    g++ \
    python3-numpy \
    gcc \
    make \
    git \
    python3-setuptools \
    python3-wheel \
    python3-pip \
    ffmpeg

WORKDIR /service

COPY requirements.txt /tmp/pip-tmp/
RUN pip --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp

ADD . /service

CMD ["gunicorn", "-c", "gunicorn.conf.py", "face_blurring.main:app"]
