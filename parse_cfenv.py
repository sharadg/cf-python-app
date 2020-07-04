import os
import urllib
from cfenv import AppEnv


rabbit_env = ""

if os.getenv("PROFILE", "CLOUD") == "LOCAL":
    # Running in a local or dev environment
    rabbit_env = "amqp://{}:{}@{}:{}/{}?heartbeat=30".format(
        os.getenv("RABBITMQ_USERNAME", "user"),
        os.getenv("RABBITMQ_PASSWORD", "bitnami"),
        os.getenv("RABBITMQ_SERVER", "localhost"),
        os.getenv("RABBITMQ_PORT", "5672"),
        urllib.parse.quote_plus(os.getenv("RABBITMQ_VHOST", "/")),
    )
else:
    cfenv = AppEnv()
    rabbit_env = cfenv.get_service(name="rabbitmq-service").get_url("uri")
    rabbit_env = rabbit_env + "?heartbeat=30"

if __name__ == "main":
    cfenv.name  # 'test-app'
    cfenv.port  # 5000

    # rabbitmq = cfenv.get_service(label='rabbitmq')
    # rabbitmq.credentials  # {'uri': '...', 'password': '...'}
    # rabbitmq.get_url(host='hostname', password='password', port='port')  # redis://pass:host
