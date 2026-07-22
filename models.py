"""
models.py
Defines the Temple data model used across the hash table, tree, and graph.
"""


class Temple:
    def __init__(self, name, category, description, built_century, location_note):
        self.name = name
        self.category = category
        self.description = description
        self.built_century = built_century
        self.location_note = location_note

    def __str__(self):
        return (
            f"{self.name}\n"
            f"  Category      : {self.category}\n"
            f"  Built         : {self.built_century}\n"
            f"  Location note : {self.location_note}\n"
            f"  About         : {self.description}"
        )