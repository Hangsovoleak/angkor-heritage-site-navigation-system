"""
hash_table.py
A hash table implemented from scratch using separate chaining.
Used to retrieve full Temple objects instantly by name.

Extras on top of the core chaining table:
    - Alias/nickname resolution ("angkor" -> "Angkor Wat") so casual
      input still finds the right entry
    - Popularity tracking: counts how many times each key has been
      looked up via get(), with a top_n() helper to rank them
"""

from temple_data import ALIASES


class HashTable:
    def __init__(self, size=17):
        self.size = size
        self.buckets = [[] for _ in range(size)]
        self.count = 0
        self.aliases = {k.strip().lower(): v for k, v in ALIASES.items()}  # nickname -> official key
        self.popularity = {}  # normalized key -> lookup count

    def _hash(self, key):
        key = key.strip().lower()
        total = sum(ord(char) for char in key)
        return total % self.size

    def _resolve_alias(self, key):
        """If `key` is a known nickname/alias, return the official key."""
        norm_key = key.strip().lower()
        return self.aliases.get(norm_key, key)

    def insert(self, key, value):
        key = self._resolve_alias(key)
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

    def get(self, key, track_popularity=True):
        key = self._resolve_alias(key)
        index = self._hash(key)
        bucket = self.buckets[index]
        norm_key = key.strip().lower()

        for existing_key, value in bucket:
            if existing_key == norm_key:
                if track_popularity:
                    self._record_lookup(norm_key)
                return value
        return None

    def __contains__(self, key):
        return self.get(key, track_popularity=False) is not None

    def _resize(self):
        old_items = [item for bucket in self.buckets for item in bucket]
        self.size *= 2
        self.buckets = [[] for _ in range(self.size)]
        self.count = 0
        for key, value in old_items:
            self.insert(key, value)

    def all_keys(self):
        return [key for bucket in self.buckets for key, _ in bucket]

    # ------------------------------------------------------------------
    # Popularity tracking
    # ------------------------------------------------------------------
    def _record_lookup(self, norm_key):
        self.popularity[norm_key] = self.popularity.get(norm_key, 0) + 1

    def track_popularity(self, key):
        """Record a lookup/use of `key` without doing a full get()."""
        key = self._resolve_alias(key)
        self._record_lookup(key.strip().lower())

    def top_n(self, n=5):
        """
        Return the n most-looked-up (key, value, count) tuples,
        most popular first.
        """
        ranked = sorted(self.popularity.items(), key=lambda item: item[1], reverse=True)
        results = []
        for norm_key, count in ranked[:n]:
            value = self.get(norm_key, track_popularity=False)
            if value is not None:
                results.append((norm_key, value, count))
        return results


def build_temple_hash_table():
    """Builds and returns a HashTable pre-loaded with all 15 temples."""
    from temple_data import TEMPLES
    ht = HashTable(size=17)
    for temple in TEMPLES.values():
        ht.insert(temple.name, temple)
    return ht


if __name__ == "__main__":
    hash_table = build_temple_hash_table()

    print("=== Alias Lookup Demo ===")
    for nickname in ["angkor", "ta prohm", "bakheng", "chau say"]:
        result = hash_table.get(nickname)
        print(f"Search '{nickname}' -> {result}")

    print("\n=== Popularity Tracker Demo ===")
    for _ in range(3):
        hash_table.get("Angkor Wat")
    for _ in range(2):
        hash_table.get("Bayon Temple")
    hash_table.get("Ta Prohm Temple")

    for norm_key, temple, count in hash_table.top_n(3):
        print(f"{temple.name}: searched {count} time(s)")