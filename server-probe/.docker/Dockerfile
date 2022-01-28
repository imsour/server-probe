FROM python:3.9.6-alpine
ENV PYTHONBUFFERED=1
WORKDIR /server-probe
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
# Database persistency
COPY probe.db /etc/probe/