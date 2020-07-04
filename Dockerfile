FROM python:3.8
LABEL maintainer="sharadgu@vmware.com"

WORKDIR /usr/src/app

COPY ["app.py", "parse_cfenv.py", "requirements.txt", "rpc_client.py", "rpc_server.py", "./"]
COPY ["./static/", "./static/"]
COPY ["./templates/", "./templates/"]

RUN apt-get update && pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080/tcp

# ENV rabbitmq.username='guest' rabbitmq.password='guest' rabbitmq.server='rabbitmq' rabbitmq.port='5672' rabbitmq.vhost='/' profile='local'

CMD ["gunicorn", "-b 0.0.0.0:8080", "-w 2", "-t 600", "app:app"]