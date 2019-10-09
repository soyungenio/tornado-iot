import logging
import os

from app.tcp_server import TCPIotServer
from tornado.ioloop import IOLoop
from tornado.options import options, define

# redis params
options.define("redis_min_con", default=5, type=int)
options.define("redis_max_con", default=10, type=int)
options.define("redis_host", default='redis', type=str)
options.define("redis_port", default=6379, type=int)
options.define('use_redis_socket', default=False,
               help='connection to redis unixsocket file', type=bool)
options.define("redis_socket", default='/var/run/redis/redis.sock', type=str)
options.define("redis_psw", default='', type=str)
options.define("redis_db", default=-1, type=int)

# aio pika params
options.define("rabbitmq_host", default=os.environ.get('RABBITMQ_HOST'), type=str)
options.define("rabbitmq_login", default=os.environ.get('RABBITMQ_USER'), type=str)
options.define("rabbitmq_psw", default=os.environ.get('RABBITMQ_PASS'), type=str)
options.define("rabbitmq_vhost", default=os.environ.get('RABBITMQ_VHOST'), type=str)


# tornado params
define("port", default=8999, help="TCP port to listen on")

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    options.parse_command_line()
    server = TCPIotServer()
    server.init_redis_pool()
    server.init_aio_pika()
    server.listen(options.port)
    logger.info("Listening on TCP port %d", options.port)
    IOLoop.current().start()
