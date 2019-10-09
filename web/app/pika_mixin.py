"""
Module contains class for work with RabbitMQ
"""
import asyncio
import logging

from aio_pika import connect_robust, IncomingMessage, Message
from tornado.options import options

logger = logging.getLogger(__name__)


class PikaApplicationMixin:
    """
    Pika controller
    """
    def __init__(self):
        self.connection = None
        self.report_exchange = None
        self.input_queue = None
        self.output_queue = None

    @property
    def rabbitmq_host(self) -> str:
        """
        Returns address for connecting to rabbitmq
        :return: str
        """
        return options.rabbitmq_host

    @property
    def rabbitmq_login(self) -> str:
        """
        Returns login for connecting to rabbitmq
        :return: str
        """
        return options.rabbitmq_login

    @property
    def rabbitmq_psw(self) -> str:
        """
        Returns password for connecting to rabbitmq
        :return: str
        """
        return options.rabbitmq_psw

    @property
    def rabbitmq_vhost(self) -> str:
        """
        Returns virtualhost for connecting to rabbitmq
        :return: str
        """
        return options.rabbitmq_vhost

    async def on_message_returned(self, message: IncomingMessage):
        """
        Execution on receipt of a message from rabbitmq

        """
        pass

    async def publish(self, body, routing_key):
        """
        Write value to queue
        :param body: message to queue
        :param routing_key: name of queue
        """
        await self.report_exchange.publish(
            Message(body=bytes(body, encoding='utf8')),
            routing_key=routing_key
        )

    def init_aio_pika(self):
        """
        Init pika connection

        """
        self.connection \
            = asyncio.get_event_loop().run_until_complete(
                self._connect()
            )

    async def _connect(self):
        """
        Init pika application

        """
        connection = await connect_robust(
            host=self.rabbitmq_host,
            login=self.rabbitmq_login,
            password=self.rabbitmq_psw,
            virtualhost=self.rabbitmq_vhost
        )

        channel = await connection.channel(publisher_confirms=False)
        self.report_exchange = await channel.declare_exchange('report', durable=True)

        self.input_queue = await channel.declare_queue('input', durable=True)
        self.output_queue = await channel.declare_queue('output', durable=True)

        await self.input_queue.bind(self.report_exchange, routing_key='input')
        await self.output_queue.bind(self.report_exchange, routing_key='output')

        await self.input_queue.consume(self.on_message_returned)

        return connection
