import logging

from aio_pika import IncomingMessage
from app.pika_mixin import PikaApplicationMixin
from app.redis_mixin import RedisApplicationMixin
from tornado.escape import json_encode, json_decode
from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer

logger = logging.getLogger(__name__)


class TCPIotServer(TCPServer, RedisApplicationMixin, PikaApplicationMixin):
    def __init__(self, ssl_options=None, **kwargs):
        self.streams = {}
        TCPServer.__init__(self, ssl_options=ssl_options, **kwargs)

    async def on_message_returned(self, message: IncomingMessage):
        """
        Execution on receipt of a message from rabbitmq

        """
        async with message.process():
            logger.info(message.body)
            json_data = json_decode(message.body)
            device_id = json_data['id']
            report = json_data['report']
            if self.streams:
                logger.info(self.streams)
                stream = self.streams[device_id]
                send_data = "@{device_id},{report}@".format(device_id=device_id, report=report)
                await stream.write(bytes(send_data, encoding='utf8'))

    def parse_incoming_data(self, data):
        """
        Parse data from tcp

        """
        str_data = data.decode("utf-8")
        list_data = str_data[1:-1].split(',')
        device_id = int(list_data[0])
        report = list_data[1]
        return device_id, report

    async def handle_stream(self, stream, address):
        """
        Execution on receipt of a message from tcp

        """
        while True:
            try:
                data = await stream.read_until_regex(b"@\w+,[A-Za-z\w\d\s\-\,\.\!]+@")
                device_id, report = self.parse_incoming_data(data)
                self.streams[device_id] = stream
                await self.set_redis_exp_val(device_id, report)
                await self.publish(json_encode({'id': device_id, 'report': report}), routing_key="input")
            except StreamClosedError:
                logger.warning("Lost client at host %s", address[0])
                break
            except Exception as e:
                logger.warning(e)
