FROM python:3.9-slim

ARG http_proxy
ARG https_proxy
ENV http_proxy=$http_proxy
ENV https_proxy=$https_proxy 

WORKDIR /app

RUN apt-get update && apt-get install -y \
    percona-toolkit \
    libdbd-mysql-perl \
    libdbi-perl \
    libio-socket-ssl-perl \
    libterm-readkey-perl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0"]
