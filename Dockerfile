FROM python:3.6

RUN apt-get update \
    && apt-get upgrade \
    && apt-get install -y --no-install-recommends \
    -y libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./
#permission issue
USER root
RUN chmod 777 -R /public/

EXPOSE 8080

CMD ["python", "/server.py"]
