from app.app import Application


def create_app():
    # Create tornado application and supply URL routes
    app = Application()

    # Init database connection
    app.init_db()

    # Init connection to rabbitmq
    app.init_aio_pika()

    # Setup HTTP Server
    app.listen(80)

    return app

