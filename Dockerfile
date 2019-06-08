FROM python:alpine3.7

WORKDIR /app

ENV PYTHONPATH=/app

COPY . /app

RUN pip install -r requirements.txt \
    && rm -rf /root/.cache

ENTRYPOINT [ "python" ]
