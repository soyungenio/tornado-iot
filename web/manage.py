import asyncio
import os

import tornado.locks
from app import Application
from tornado.options import options

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


def main():
    # Create tornado application and supply URL routes
    app = Application()

    # Init database connection
    app.init_db()

    # Init connection to rabbitmq
    app.init_aio_pika()

    # Setup HTTP Server
    app.listen(80)

    return app


if __name__ == "__main__":
    main()
    tornado.ioloop.IOLoop.current().start()
