import tornado.web
from aio_pika import IncomingMessage
from tornado.escape import json_decode

from .database import Database
from .handlers import DeviceHandler, ReportHandler
from .pika_mixin import PikaApplicationMixin
from .tables import report


class Application(tornado.web.Application, Database, PikaApplicationMixin):
    def __init__(self):
        handlers = (
            (r'/api/v1/device', DeviceHandler),
            (r'/api/v1/device/(?P<id>\w+)/reports', ReportHandler)
        )
        tornado.web.Application.__init__(self, handlers, debug=True, autoreload=True)

    async def on_message_returned(self, message: IncomingMessage):
        """
        Execution on receipt of a message from rabbitmq

        """
        async with message.process():
            json_data = json_decode(message.body)
            await self.query(report.insert().values(device_id=json_data['id'],
                                                    report=json_data['report']))