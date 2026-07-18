"""
hash_table.py
A hash table implemented from scratch using separate chaining.
Used to retrieve full Temple objects instantly by name.
"""


class HashTable:
    def __init__(self, size=17):
        self.size = size
        self.buckets = [[] for _ in range(size)]
        self.count = 0

    def _hash(self, key):
        key = key.strip().lower()
        total = sum(ord(char) for char in key)
        return total % self.size

    def insert(self, key, value):
        index = self._hash(key)
        bucket = self.buckets[index]
        norm_key = key.strip().lower()

        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == norm_key:
                bucket[i] = (norm_key, value)
                return

        bucket.append((norm_key, value))
        self.count += 1

        # Resize if the average chain length gets too long, to keep lookups near O(1)
        if self.count / self.size > 1.5:
            self._resize()

    def get(self, key):
        index = self._hash(key)
        bucket = self.buckets[index]
        norm_key = key.strip().lower()

        for existing_key, value in bucket:
            if existing_key == norm_key:
                return value
        return None

    def __contains__(self, key):
        return self.get(key) is not None

    def _resize(self):
        old_items = [item for bucket in self.buckets for item in bucket]
        self.size *= 2
        self.buckets = [[] for _ in range(self.size)]
        self.count = 0
        for key, value in old_items:
            self.insert(key, value)

    def all_keys(self):
        return [key for bucket in self.buckets for key, _ in bucket]