"""
Angkor Heritage Site Navigation System
---------------------------------------
Shared temple data.

Every module (hash table, tree, graph) references the SAME 15 temples and
the SAME numeric IDs (1-15), matching the legend used in the project's
graph diagram. Keeping one source of truth avoids ID mismatches between
the hash table, tree, and graph.
"""


class Temple:
    """Represents a single temple (the data stored/looked-up in the system)."""

    def __init__(self, temple_id, name, category, distance_from_angkor_wat):
        self.temple_id = temple_id
        self.name = name
        self.category = category
        self.distance_from_angkor_wat = distance_from_angkor_wat

    def __repr__(self):
        return (f"[ID:{self.temple_id}] {self.name} "
                f"({self.category}, {self.distance_from_angkor_wat} km from Angkor Wat)")


# ID -> Temple, matching the numbering used in the graph diagram legend
TEMPLES = {
    1: Temple(1, "Angkor Wat", "Main Temple", 0.0),
    2: Temple(2, "Bayon Temple", "Main Temple", 3.5),
    3: Temple(3, "Ta Prohm Temple", "Jungle Temple", 7.0),
    4: Temple(4, "Preah Khan Temple", "Historic Temple", 8.5),
    5: Temple(5, "Banteay Srei", "Outlying Temple", 32.0),
    6: Temple(6, "Phnom Bakheng Temple", "Hilltop Temple", 1.3),
    7: Temple(7, "Baphuon Temple", "Historic Temple", 4.0),
    8: Temple(8, "Pre Rup Temple", "Outlying Temple", 13.0),
    9: Temple(9, "Banteay Kdei Temple", "Historic Temple", 7.5),
    10: Temple(10, "Ta Som", "Outlying Temple", 14.0),
    11: Temple(11, "Neak Poan Temple", "Outlying Temple", 11.5),
    12: Temple(12, "Eastern Mebon Temple", "Outlying Temple", 14.5),
    13: Temple(13, "Ta Keo Temple", "Historic Temple", 6.5),
    14: Temple(14, "Prasat Chau Say Tevoda", "Historic Temple", 6.0),
    15: Temple(15, "Thommanon Temple", "Historic Temple", 6.0),
}

# Undirected weighted edges (temple_id, temple_id, distance_km), taken from
# the project's graph diagram.
EDGES = [
    (4, 11, 2.2),
    (11, 10, 3.0),
    (4, 14, 2.5),
    (14, 11, 5.1),
    (4, 2, 3.1),
    (14, 15, 0.15),
    (2, 15, 1.2),
    (2, 6, 1.8),
    (2, 1, 1.6),
    (6, 1, 1.5),
    (15, 13, 1.0),
    (13, 3, 0.9),
    (13, 12, 5.8),
    (10, 12, 6.5),
    (10, 5, 15.8),
    (12, 8, 1.5),
    (8, 5, 19.5),
    (3, 9, 1.0),
    (3, 1, 2.8),
    (9, 8, 2.0),
    (9, 7, 2.3),
    (1, 7, 2.9),
]


# Common nicknames / shorthand / misspellings -> the temple's official name.
# Lets the Hash Table forgive casual input like "angkor" or "ta prohm" (Tomb
# Raider temple) instead of requiring the exact full name.
ALIASES = {
    "angkor": "Angkor Wat",
    "angkor wat temple": "Angkor Wat",
    "bayon": "Bayon Temple",
    "ta prohm": "Ta Prohm Temple",
    "tomb raider temple": "Ta Prohm Temple",
    "preah khan": "Preah Khan Temple",
    "banteay srei temple": "Banteay Srei",
    "phnom bakheng": "Phnom Bakheng Temple",
    "bakheng": "Phnom Bakheng Temple",
    "baphuon": "Baphuon Temple",
    "pre rup": "Pre Rup Temple",
    "banteay kdei": "Banteay Kdei Temple",
    "ta som temple": "Ta Som",
    "neak poan": "Neak Poan Temple",
    "eastern mebon": "Eastern Mebon Temple",
    "east mebon": "Eastern Mebon Temple",
    "ta keo": "Ta Keo Temple",
    "chau say tevoda": "Prasat Chau Say Tevoda",
    "chau say": "Prasat Chau Say Tevoda",
    "thommanon": "Thommanon Temple",
    "ta prohrn": "Ta Prohm Temple",  # typo seen in the original doc
}


def name_to_id(name):
    """Look up a temple's ID from its name (case-insensitive)."""
    name_norm = name.strip().lower()
    for temple_id, temple in TEMPLES.items():
        if temple.name.lower() == name_norm:
            return temple_id
    return None
