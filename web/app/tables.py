import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

metadata = sa.MetaData()
Base = declarative_base()


device = sa.Table('device', metadata,
                  sa.Column('id', sa.Integer, primary_key=True),
                  sa.Column('device_id', sa.Integer(), nullable=False))

report = sa.Table('report', metadata,
                  sa.Column('id', sa.Integer, primary_key=True),
                  sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.current_timestamp()),
                  sa.Column('report', sa.String(36), nullable=False),
                  sa.Column('device_id', sa.Integer(), nullable=False))
