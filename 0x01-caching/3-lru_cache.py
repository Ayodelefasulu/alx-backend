#!/usr/bin/python3
""" LRUCache module """

from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """ LRU Caching system that inherits from BaseCaching """

    def __init__(self):
        """ Initialize by calling the parent class's __init__ """
        super().__init__()
        self.keys_order = []  # Track the order of access for LRU algorithm

    def put(self, key, item):
        """ Add an item in the cache using LRU algorithm """
        if key is None or item is None:
            return

        # If key is already in cache, update its value and move it to the most
        # recently used
        if key in self.cache_data:
            self.cache_data[key] = item
            self.keys_order.remove(key)
            self.keys_order.append(key)
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Discard the least recently used item (LRU)
                lru_key = self.keys_order.pop(0)  # Remove the first item (LRU)
                print(f"DISCARD: {lru_key}")
                del self.cache_data[lru_key]

            # Add the new key-value pair to cache and update access order
            self.cache_data[key] = item
            self.keys_order.append(key)

    def get(self, key):
        """ Get an item by key from the cache and update its access order """
        if key is None or key not in self.cache_data:
            return None

        # Update key's access to the most recently used position
        self.keys_order.remove(key)
        self.keys_order.append(key)
        return self.cache_data[key]
