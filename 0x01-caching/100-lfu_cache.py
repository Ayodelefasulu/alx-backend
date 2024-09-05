#!/usr/bin/python3
""" LFUCache module """

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ LFU Caching system that inherits from BaseCaching """

    def __init__(self):
        """ Initialize by calling the parent class's __init__ """
        super().__init__()
        self.freq = {}  # Dictionary to store the frequency of each key
        # List to maintain access order (for LRU tie-breaker)
        self.keys_order = []

    def put(self, key, item):
        """ Add item in cache using LFU algorithm with LRU tie-breaker """
        if key is None or item is None:
            return

        # If key is already in cache, update its value and frequency
        if key in self.cache_data:
            self.cache_data[key] = item
            self.freq[key] += 1
            self.keys_order.remove(key)
            self.keys_order.append(key)
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Find the least frequently used key
                min_freq = min(self.freq.values())
                lfu_keys = [k for k, v in self.freq.items() if v == min_freq]

                # If there is a tie, use LRU (least recently used)
                if len(lfu_keys) > 1:
                    for k in self.keys_order:
                        if k in lfu_keys:
                            key_to_discard = k
                            break
                else:
                    key_to_discard = lfu_keys[0]

                # Discard the least frequently used (or LRU in case of tie)
                print(f"DISCARD: {key_to_discard}")
                del self.cache_data[key_to_discard]
                del self.freq[key_to_discard]
                self.keys_order.remove(key_to_discard)

            # Add the new key-value pair to cache, set frequency, and update
            # access order
            self.cache_data[key] = item
            self.freq[key] = 1
            self.keys_order.append(key)

    def get(self, key):
        """ Get item by key from cache, update its frequency, access order """
        if key is None or key not in self.cache_data:
            return None

        # Update the frequency and access order
        self.freq[key] += 1
        self.keys_order.remove(key)
        self.keys_order.append(key)
        return self.cache_data[key]
