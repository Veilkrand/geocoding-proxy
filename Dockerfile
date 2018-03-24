FROM ubuntu:latest
MAINTAINER Alberto Naranjo "alberto.galet@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /geocoding-proxy
WORKDIR /geocoding-proxy
RUN pip install -r requirements.txt
WORKDIR /geocoding-proxy/app
ENTRYPOINT ["python"]
CMD ["app.py"]