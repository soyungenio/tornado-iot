from marshmallow import Schema, fields, EXCLUDE


class DeviceSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(reqired=True)
