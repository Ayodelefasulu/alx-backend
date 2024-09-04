#!/usr/bin/python3
"""
The basic cache module
"""


from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """ BasicCache defines a basic caching system with no limit. """

    def put(self, key, item):
        """ Assign the item to the dictionary self.cache_data with the key.
        If key or item is None, this method should not do anything.
        """
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        """ Return the value in self.cache_data linked to key.
        If key is None or if the key doesn’t exist in self.cache_data,
        return None.
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
        # return self.cache_data.get(key, None)
