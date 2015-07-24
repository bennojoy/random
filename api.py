#!/usr/bin/env python

from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.httpserver
import redis
import os
import json
from random import randint

dirname = os.path.dirname(__file__)

class GetRandomFortune(tornado.web.RequestHandler):

    def get(self):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        category_index = randint(0, int(r.llen('categories')))
        category_index = category_index - 1
        category       = r.lrange('categories', category_index, category_index)[0]
        max_items = r.get(category)
        random_index = randint(0, int(max_items))
        random_hash_index = int(random_index / 1000)

        if random_hash_index == 0:
            random_index_number = random_index
        else:
            random_index_number = random_index - (1000 * random_hash_index)

        fortune = r.hget(category + '_' + str(random_hash_index), random_index_number)
        response = { 'fortune': fortune}
        self.write(json.dumps(response))

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
 
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/api/fortune", GetRandomFortune)
        ]
        settings = {
            "template_path": os.path.join(dirname, 'templates'),
            "static_path": os.path.join(dirname, 'static'),
        }
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    
    applicaton = Application()
    http_server = tornado.httpserver.HTTPServer(applicaton)
    http_server.listen(7777)
    tornado.ioloop.IOLoop.instance().start()

