import asyncio
import os

from app import create_app
import tornado.locks
from tornado.options import options
import pytest
import click

# pika params
options.define("rabbitmq_host", default=os.environ.get('RABBITMQ_HOST'), type=str)
options.define("rabbitmq_login", default=os.environ.get('RABBITMQ_USER'), type=str)
options.define("rabbitmq_psw", default=os.environ.get('RABBITMQ_PASS'), type=str)
options.define("rabbitmq_vhost", default=os.environ.get('RABBITMQ_VHOST'), type=str)

# database params
options.define("postgres_host", default=os.environ.get('POSTGRES_HOST'), type=str)
options.define("postgres_login", default=os.environ.get('POSTGRES_USER'), type=str)
options.define("postgres_psw", default=os.environ.get('POSTGRES_PASSWORD'), type=str)
options.define("postgres_db", default=os.environ.get('POSTGRES_DB'), type=str)

tornado.ioloop.IOLoop.configure('tornado.platform.asyncio.AsyncIOLoop')
io_loop = tornado.ioloop.IOLoop.current()
asyncio.set_event_loop(io_loop.asyncio_loop)


@click.group()
def main():
    pass


@main.command("test")
def test():
    pytest.main(["-x", "tests"])


@main.command("start")
def start():
    create_app()
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
