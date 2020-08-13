FROM python:3.6

ENV BFF_ENDPOINT=http://covid-tracer-bff-node-covid-tracker.sandbox-ocp431-one-89dadfe96916fcd27b299431d0240c37-0000.eu-gb.containers.appdomain.cloud/

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

CMD ["python", "/app.py"]
