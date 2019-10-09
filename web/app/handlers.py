import json
import logging
import time

from marshmallow import ValidationError
from sqlalchemy import desc
from tornado.escape import json_decode

from .base_handler import BaseHandler
from .schemas import DeviceSchema
from .tables import device, report

logger = logging.getLogger(__name__)


class DeviceHandler(BaseHandler):
    def set_default_headers(self, *args, **kwargs):
        self.set_header('Content-Type', 'application/json')

    async def post(self):
        json_data = json_decode(self.request.body)

        # validate and deserialize input
        device_scheme = DeviceSchema()
        try:
            device_scheme.load(json_data)
        except ValidationError as err:
            self.set_status(400)
            await self.finish(json.dumps({"message": err.messages}))

        await self.query(device.insert().values(id=json_data['id']))


class ReportHandler(BaseHandler):
    def set_default_headers(self, *args, **kwargs):
        self.set_header('Content-Type', 'application/json')

    async def get(self, id):
        query_result = await self.query(report.select().where(report.c.device_id == id).
                                           order_by(desc("created_at")))

        response = {
            "reports": []
        }
        for row in query_result:
            report_row = dict()
            report_row['timestamp'] = time.mktime(row.created_at.timetuple())
            report_row['report'] = row.report
            response['reports'].append(report_row)

        await self.finish(json.dumps(response))

    async def post(self, id):
        json_data = json_decode(self.request.body)

        # validate and deserialize input
        device_scheme = DeviceSchema()
        try:
            device_scheme.load(json_data)
        except ValidationError as err:
            self.set_status(400)
            await self.finish(json.dumps({"message": err.messages}))

        await self.pika_publish(json.dumps(json_data), routing_key="output")
