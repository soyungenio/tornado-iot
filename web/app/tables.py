import sqlalchemy as sa

metadata = sa.MetaData()

device = sa.Table('device', metadata,
                  sa.Column('id', sa.Integer, primary_key=True))

report = sa.Table('report', metadata,
                  sa.Column('id', sa.Integer, primary_key=True),
                  sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.current_timestamp()),
                  sa.Column('report', sa.String(36), nullable=False),
                  sa.Column('device_id', None, sa.ForeignKey('device.id')))
