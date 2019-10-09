import tornado


class BaseHandler(tornado.web.RequestHandler):
    def query(self, table_object):
        """
        Query to database
        :param table_object: object containing table
        :return: list
        """
        return self.application.query(table_object)

    def queryone(self, table_object):
        """
        Query to database
        :param table_object: object containing table
        :return: dict
        """
        return self.application.queryone(table_object)

    def pika_publish(self, body, routing_key):
        """
        Write value to queue
        :param body: message to queue
        :param routing_key: name of queue
        """
        return self.application.publish(body, routing_key)