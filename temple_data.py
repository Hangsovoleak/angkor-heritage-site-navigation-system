"""
temple_data.py
Predefined data for 15 temples in the Angkor Archaeological Park (Cambodia):
their info, common aliases, category groupings, and the distances between them.

Note: distances are approximate, illustrative road distances for this
project's demo dataset, not surveyed GPS measurements.
"""

from models import Temple
from hash_table import HashTable
from tree import CategoryTree
from graph import Graph

TEMPLES = [
    Temple(1, "Angkor Wat", "State temple",
           "The largest religious monument in the world, built as a Hindu temple "
           "and later transformed into a Buddhist site.",
           "12th century", "South of Angkor Thom"),
    Temple(2, "Bayon", "State temple",
           "Known for its many serene, giant stone faces carved into its towers.",
           "Late 12th - early 13th century", "Center of Angkor Thom"),
    Temple(3, "Baphuon", "State temple",
           "A three-tiered temple mountain with a giant reclining Buddha built "
           "into its western side.",
           "11th century", "Inside Angkor Thom, near the Royal Palace"),
    Temple(4, "Phnom Bakheng", "State temple",
           "A hilltop temple popular for sunset views over Angkor Wat.",
           "9th - 10th century", "Small hill between Angkor Wat and Angkor Thom"),
    Temple(5, "Pre Rup", "State temple",
           "A temple mountain of brick, laterite, and sandstone, used for "
           "royal cremation rituals.",
           "10th century", "East of the East Baray"),
    Temple(6, "East Mebon", "State temple",
           "A temple mountain originally built on an artificial island in the "
           "now-dry East Baray reservoir.",
           "10th century", "Near Pre Rup"),
    Temple(7, "Ta Keo", "State temple",
           "An unfinished temple mountain known for its stark, undecorated "
           "sandstone blocks.",
           "Late 10th - early 11th century", "Near Ta Prohm"),
    Temple(8, "Ta Prohm", "Monastery",
           "Famous for large trees growing through its ruins; kept largely "
           "in its 'as found' state.",
           "Late 12th - early 13th century", "East of Angkor Thom"),
    Temple(9, "Preah Khan", "Monastery",
           "A large monastic and teaching complex with long processional "
           "causeways.",
           "12th century", "North of Angkor Thom"),
    Temple(10, "Banteay Kdei", "Monastery",
           "A quiet Buddhist monastic complex with a labyrinth-like layout.",
           "12th century", "East of Ta Prohm"),
    Temple(11, "Banteay Srei", "Monastery",
           "A small, intricately carved temple known for detailed pink "
           "sandstone reliefs.",
           "10th century", "Northeast of the main Angkor complex"),
    Temple(12, "Neak Pean", "Water temple",
           "A small island temple set in a square pool, historically used "
           "for ritual purification.",
           "Late 12th century", "Near Preah Khan"),
    Temple(13, "Srah Srang", "Water temple",
           "A royal bathing pool with a sandstone landing platform.",
           "10th century (rebuilt 12th)", "East of Banteay Kdei"),
    Temple(14, "Terrace of the Elephants", "Royal structure",
           "A long public viewing terrace decorated with carved elephants, "
           "used by the king to view public ceremonies.",
           "Late 12th century", "Inside Angkor Thom"),
    Temple(15, "Beng Mealea", "Royal structure",
           "A large, largely unrestored temple complex surrounded by jungle, "
           "similar in layout to Angkor Wat.",
           "12th century", "Roughly 40 km east of the main Angkor complex"),
]

# Nicknames a user might type instead of the full name
ALIASES = {
    "angkor": "Angkor Wat",
    "wat": "Angkor Wat",
    "bakheng": "Phnom Bakheng",
    "prohm": "Ta Prohm",
    "ta prohm": "Ta Prohm",
    "srei": "Banteay Srei",
    "banteay srei": "Banteay Srei",
    "kdei": "Banteay Kdei",
    "khan": "Preah Khan",
    "preah khan": "Preah Khan",
    "mebon": "East Mebon",
    "mealea": "Beng Mealea",
    "srang": "Srah Srang",
    "keo": "Ta Keo",
    "pean": "Neak Pean",
    "elephants": "Terrace of the Elephants",
    "terrace": "Terrace of the Elephants",
}

# (temple_a, temple_b, distance_km) - approximate, for demo purposes
DISTANCES = [
    ("Angkor Wat", "Bayon", 3.0),
    ("Angkor Wat", "Phnom Bakheng", 2.0),
    ("Bayon", "Baphuon", 0.5),
    ("Baphuon", "Terrace of the Elephants", 0.3),
    ("Bayon", "Terrace of the Elephants", 0.6),
    ("Terrace of the Elephants", "Ta Keo", 1.0),
    ("Ta Keo", "Ta Prohm", 2.5),
    ("Ta Prohm", "Banteay Kdei", 1.5),
    ("Banteay Kdei", "Srah Srang", 0.5),
    ("Srah Srang", "Pre Rup", 3.0),
    ("Pre Rup", "East Mebon", 2.0),
    ("East Mebon", "Neak Pean", 4.0),
    ("Neak Pean", "Preah Khan", 2.5),
    ("Preah Khan", "Angkor Wat", 5.0),
    ("Bayon", "Preah Khan", 3.0),
    ("Angkor Wat", "Banteay Srei", 25.0),
    ("Banteay Srei", "Preah Khan", 20.0),
    ("Banteay Srei", "Beng Mealea", 40.0),
    ("Beng Mealea", "Preah Khan", 45.0),
    ("Ta Keo", "Beng Mealea", 42.0),
]


def build_hash_table():
    table = HashTable(size=17, aliases=ALIASES)
    for temple in TEMPLES:
        table.insert(temple.name, temple)
    return table


def build_category_tree():
    tree = CategoryTree()
    for temple in TEMPLES:
        tree.add_temple_to_category(temple.category, temple.name)
    return tree


def build_graph():
    graph = Graph()
    for temple in TEMPLES:
        graph.add_temple(temple.name)
    for temple_a, temple_b, distance in DISTANCES:
        graph.add_edge(temple_a, temple_b, distance)
    return graph