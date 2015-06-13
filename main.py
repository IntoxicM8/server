import tornado.ioloop
import tornado.web

from handlers import *

application = tornado.web.Application([
    (r"/users/?", UserHandler),
    (r"/data/?", DataHandler),
    (r"/confirms/?", ConfirmHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
