import sys
import uuid
import time
import pika
from parse_cfenv import rabbit_env


class FibonacciRPCClient(object):
    def __init__(self):
        self._connection_params = pika.URLParameters(rabbit_env)
        self._connection = None
        self._outstanding_requests = {}
        self.connect()

    def connect(self):
        if not self._connection or self._connection.is_closed:
            self._connection = pika.BlockingConnection(self._connection_params)
            self._channel = self._connection.channel()
            result = self._channel.queue_declare('', exclusive=True)
            self._callback_queue = result.method.queue
            self._channel.basic_consume(queue=self._callback_queue, on_message_callback=self.on_response, auto_ack=True)
            self._connection.process_data_events()

    def on_response(self, ch, method, properties, body):
        if properties.correlation_id in self._outstanding_requests:
            self._outstanding_requests[properties.correlation_id] = body
            sys.stderr.write('received response message with correlation id: {}\n'.format(properties.correlation_id))

    def _publish(self, msg, correlation_id, exchange='', routing_key='rpc_queue'):
        self._channel.basic_publish(exchange=exchange,
                                    routing_key=routing_key,
                                    properties=pika.BasicProperties(
                                        reply_to=self._callback_queue,
                                        correlation_id=correlation_id),
                                    body=str(msg))
        sys.stderr.write('sending request message with correlation id: {}\n'.format(correlation_id))

    def call(self, msg):
        corr_id = str(uuid.uuid4())
        self._outstanding_requests[corr_id] = None

        try:
            self._publish(msg, correlation_id=corr_id)
        except pika.exceptions.AMQPConnectionError:
            sys.stderr.write('Reconnecting...\n')
            time.sleep(0.2)
            self.connect()
            self._publish(msg, correlation_id=corr_id)

        while self._outstanding_requests[corr_id] is None:
            self._connection.process_data_events()

        response = self._outstanding_requests[corr_id]
        del self._outstanding_requests[corr_id]
        return int(response)


if __name__ == "__main__":
    fibonacci_rpc = FibonacciRPCClient()
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    print(' [*] Requesting fib({})'.format(n))
    response = fibonacci_rpc.call(n)
    print(' [.] Got {}'.format(response))
