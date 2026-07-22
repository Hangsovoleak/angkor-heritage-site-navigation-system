"""
hash_table.py
A hash table built from scratch using separate chaining.

Supports lookup by exact key, by a registered numeric ID, or by an
alias/nickname - e.g. a temple can be found by its full name ("Angkor
Wat"), its ID ("1"), or a short nickname ("angkor").
"""


class HashTable:
    def __init__(self, size=17, aliases=None):
        self.size = size
        self.buckets = [[] for _ in range(size)]
        self.count = 0
        self.aliases = {k.strip().lower(): v for k, v in (aliases or {}).items()}
        self.id_index = {}  # str(id) -> normalized key, for ID-based search

    def _hash(self, key):
        key = key.strip().lower()
        return sum(ord(char) for char in key) % self.size

    def _resolve(self, key):
        """Turn an ID or alias into the canonical key it points to."""
        key_str = str(key).strip()
        if key_str in self.id_index:
            return self.id_index[key_str]
        return self.aliases.get(key_str.lower(), key_str)

    def insert(self, key, value):
        key = self._resolve(key)
        norm_key = key.strip().lower()
        index = self._hash(norm_key)
        bucket = self.buckets[index]

        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == norm_key:
                bucket[i] = (norm_key, value)
                return

        bucket.append((norm_key, value))
        self.count += 1

        entry_id = getattr(value, "temple_id", None)
        if entry_id is not None:
            self.id_index[str(entry_id)] = norm_key

    def get(self, key):
        key = self._resolve(key)
        norm_key = key.strip().lower()
        index = self._hash(norm_key)

        for existing_key, value in self.buckets[index]:
            if existing_key == norm_key:
                return value
        return None

    def __contains__(self, key):
        return self.get(key) is not None

    def display(self):
        """
        Print every stored entry with its bucket index and the hash
        function's output, so the user can see what's stored and how
        each key maps to a bucket - both a search reference and a
        demonstration of the hash function itself.
        """
        print(f"\n{'Bucket':<8}{'ID':<5}{'Name (search key)':<26}{'hash(key)'}")
        print("-" * 60)
        for index in range(self.size):
            for key, value in self.buckets[index]:
                entry_id = getattr(value, "temple_id", "-")
                name = getattr(value, "name", key)
                print(f"{index:<8}{entry_id:<5}{name:<26}hash('{key}') = {index}")
        print(f"\n{self.count} temple(s) stored across {self.size} buckets "
              f"(load factor {self.count / self.size:.2f}).")
        print("Search by ID, full name, or a known alias (e.g. 'angkor', 'srei').")