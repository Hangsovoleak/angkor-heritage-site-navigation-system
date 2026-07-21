"""
hash_table.py
A hash table implemented from scratch using separate chaining.
Used to retrieve full Temple objects instantly by name.

Extras on top of the core chaining table:
    - Alias/nickname resolution ("angkor" -> "Angkor Wat") so casual
      input still finds the right entry
    - Popularity tracking: counts how many times each key has been
      looked up via get(), with a top_n() helper to rank them
    - ID lookup: users can search by a temple's numeric ID (e.g. "3")
      as well as by name - get() accepts either
    - display(): shows bucket index, key (name), and ID together so
      users can see how to search either way
"""

from temple_data import ALIASES


class HashTable:
    def __init__(self, size=17):
        self.size = size
        self.buckets = [[] for _ in range(size)]
        self.count = 0
        self.aliases = {k.strip().lower(): v for k, v in ALIASES.items()}  # nickname -> official key
        self.popularity = {}  # normalized key -> lookup count
        self.id_index = {}    # temple_id (str) -> normalized name key, for ID-based search

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

        # If the value carries a temple_id, register it so users can
        # also search by ID (e.g. "3") instead of typing the full name
        temple_id = getattr(value, "temple_id", None)
        if temple_id is not None:
            self.id_index[str(temple_id)] = norm_key

        # Resize if the average chain length gets too long, to keep lookups near O(1)
        if self.count / self.size > 1.5:
            self._resize()

    def get(self, key, track_popularity=True):
        # Allow searching by numeric ID (e.g. "3" or 3) in addition to name
        key_str = str(key).strip()
        if key_str in self.id_index:
            key = self.id_index[key_str]

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
    # Display
    # ------------------------------------------------------------------
    def display(self):
        """
        Print every stored entry showing bucket index, key (name), and
        ID together - so users can see they're free to search by either
        the temple's name or its numeric ID.
        """
        print(f"{'Bucket':<8}{'ID':<5}{'Name (search key)':<26}{'Details'}")
        print("-" * 80)
        for index, bucket in enumerate(self.buckets):
            for key, value in bucket:
                temple_id = getattr(value, "temple_id", "-")
                name = getattr(value, "name", key)
                print(f"{index:<8}{temple_id:<5}{name:<26}{value}")

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

    # ------------------------------------------------------------------
    # Summary / performance stats
    # ------------------------------------------------------------------
    def summary(self):
        """
        Return a dict of stats describing the table's current state -
        useful for demonstrating hash table performance (load factor,
        collision spread, etc.) in a presentation.
        """
        chain_lengths = [len(bucket) for bucket in self.buckets]
        used_buckets = [length for length in chain_lengths if length > 0]
        collided_buckets = [length for length in chain_lengths if length > 1]

        total_lookups = sum(self.popularity.values())
        most_searched = self.top_n(1)

        return {
            "size": self.size,                                  # number of buckets
            "count": self.count,                                # number of stored entries
            "load_factor": round(self.count / self.size, 3),
            "empty_buckets": chain_lengths.count(0),
            "used_buckets": len(used_buckets),
            "buckets_with_collisions": len(collided_buckets),
            "longest_chain": max(chain_lengths) if chain_lengths else 0,
            "average_chain_length_used": (
                round(sum(used_buckets) / len(used_buckets), 2) if used_buckets else 0
            ),
            "total_lookups_recorded": total_lookups,
            "most_searched": most_searched[0] if most_searched else None,  # (key, value, count)
        }

    def print_summary(self):
        """Pretty-print the summary() stats to the terminal."""
        stats = self.summary()

        print("=== Hash Table Summary ===")
        print(f"Buckets (table size):     {stats['size']}")
        print(f"Entries stored:           {stats['count']}")
        print(f"Load factor:              {stats['load_factor']}")
        print(f"Empty buckets:            {stats['empty_buckets']}")
        print(f"Used buckets:             {stats['used_buckets']}")
        print(f"Buckets with collisions:  {stats['buckets_with_collisions']}")
        print(f"Longest chain:            {stats['longest_chain']}")
        print(f"Avg chain length (used):  {stats['average_chain_length_used']}")
        print(f"Total lookups recorded:   {stats['total_lookups_recorded']}")

        if stats["most_searched"]:
            _, value, count = stats["most_searched"]
            name = getattr(value, "name", value)
            print(f"Most searched entry:      {name} ({count} lookup(s))")
        else:
            print("Most searched entry:      (no lookups recorded yet)")


def build_temple_hash_table():
    """Builds and returns a HashTable pre-loaded with all 15 temples."""
    from temple_data import TEMPLES
    ht = HashTable(size=17)
    for temple in TEMPLES.values():
        ht.insert(temple.name, temple)
    return ht


if __name__ == "__main__":
    hash_table = build_temple_hash_table()

    print("=== Table Display (name + ID together) ===")
    hash_table.display()

    print("\n=== Search by Name vs Search by ID ===")
    print(f"Search by name 'Bayon Temple' -> {hash_table.get('Bayon Temple')}")
    print(f"Search by ID   '2'            -> {hash_table.get('2')}")

    print("\n=== Alias Lookup Demo ===")
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

    print("\n" + "=" * 30)
    hash_table.print_summary()
