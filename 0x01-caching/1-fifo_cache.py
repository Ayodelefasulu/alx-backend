#!/usr/bin/python3
"""
The FIFO cache module
"""


from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ FIFO Caching system that inherits from BaseCaching """

    def __init__(self):
        """ Initialize by calling the parent class's __init__ """
        super().__init__()

    def put(self, key, item):
        """ Add an item in the cache using FIFO algorithm """
        self.cache_data[key] = item

        if key is None or item is None:
            return
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            index = list(self.cache_data)
            index_0 = index[0]
            print("DISCARD: {}".format(index_0))
            self.cache_data.pop(index_0)

    def get(self, key):
        """ Get an item by key from the cache """
        if key is None or key not in self.cache_data:
            return None
        return self.cache[key]
