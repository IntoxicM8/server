import tornado.ioloop
from tornado.web import Application, url
import tornado.httpserver
import tornado.ioloop

import logging

from handlers import *


class App(Application):
    def __init__(self, **overrides):
        handlers = [
            (r"/users/?", UserHandler),
            (r"/data/?", DataHandler),
            (r"/confirms/?", ConfirmHandler),
        ]

        Application.__init__(self, handlers)
        self.client = MongoClient('ds063140.mongolab.com', 63140)


if __name__ == "__main__":
    logging.info('running shit')

    application = App()
    http_server = tornado.httpserver.HTTPServer(application)

    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
