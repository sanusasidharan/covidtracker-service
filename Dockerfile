FROM python:3.8

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    -y libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

#WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./


EXPOSE 8000

CMD ["python", "/server.py"]
