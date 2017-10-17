# -*- coding: utf-8 -*-

from werkzeug.contrib.cache import MemcachedCache, NullCache
from flask import current_app as app


class CacheContainer:
    def __init__(self):
        pass

    def get_cache(self):
        if not hasattr(app, 'cache'):
            app.cache = self.connect()
        return app.cache

    def connect(self):
        try:
            conf = app.config.get('MEMCACHED')
            cache = MemcachedCache(**conf)
        except:
            cache = NullCache()

        return cache
