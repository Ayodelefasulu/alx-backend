#!/usr/bin/python3
"""
The LIFO cache module
"""


from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ LIFO Caching system that inherits from BaseCaching """

    def __init__(self):
        """ Initialize by calling the parent class's __init__ """
        super().__init__()

    def put(self, key, item):
        """ Add an item in the cache using LIFO algorithm """
        self.cache_data[key] = item

        if key is None or item is None:
            return
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            """indexes = list(self.cache_data)
            index_1_rev = indexes[-1]
            iterator = iter(index_1_rev)
            print("DISCARD: {}".format(next(iterator)))
            self.cache_data.pop(next(iterator))
            """
            if self.last_key is not None:
                print(f"DISCARD: {self.last_key}")
                del self.cache_data[self.last_key]

        # Add the new item and update the last inserted key
        self.cache_data[key] = item
        self.last_key = key

    def get(self, key):
        """ Get an item by key from the cache """
        if key is None or key not in self.cache_data:
            return None
        return self.cache[key]
