FROM python:3.9.14-buster

WORKDIR /service

COPY requirements.txt /tmp/pip-tmp/
RUN pip --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp

ADD . /service

CMD ["gunicorn", "-c", "gunicorn.conf.py", "face_blurring.main:app"]
