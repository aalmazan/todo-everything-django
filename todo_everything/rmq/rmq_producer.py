import logging
import os
import time

import pika
from django.conf import settings

# connection = pika.BlockingConnection()
# channel = connection.channel()
# channel.basic_publish(exchange="test", routing_key="test", body=b"Test message.")
# connection.close()

logging.basicConfig()
logger = logging.getLogger(__name__)


class RMQProducer(object):
    channel = None
    connection = None

    def __init__(self):
        # TODO: Fix hardcoded rmq URL
        url = os.environ.get("CLOUDAMQP_URL", "amqp://guest:guest@rabbitmq:5672/")
        # url = settings.CELERY_BROKER_URL
        params = pika.URLParameters(url)
        params.socket_timeout = 5
        self.connection = pika.BlockingConnection(params)  # Connect to CloudAMQP
        self.channel = self.connection.channel()  # start a channel
        self.channel.queue_declare(queue=settings.RMQ_QUEUE_NAME)  # Declare a queue

    def publish(self):
        # TODO: Update to real things
        logger.info("RMQPRODUCER - publish")
        for x in range(100):
            # Message to send to rabbitmq
            bodys = "data ke " + str(x + 1)

            self.channel.basic_publish(
                exchange="", routing_key="pdfprocess", body=bodys
            )
            logger.info("[x] Message sent to consumer = " + bodys)
            a = x % 10
            if a == 0:
                time.sleep(1)

    def close(self):
        if self.connection:
            self.connection.close()
