"""
tree.py
Category tree for the Angkor temples.

    Root ("Angkor Temples")
      -> Category node (e.g. "Water temple")
           -> Temple leaf node (e.g. "Neak Pean")

display_all()          - the full tree: every category, every temple
display_category(name) - just one category's branch
get_related_temples()  - other temples sharing a category, used by
                          main.py to recommend "nearby" temples after a search
"""


class Node:
    def __init__(self, label):
        self.label = label
        self.children = []

    def add_child(self, node):
        self.children.append(node)
        return node


class CategoryTree:
    def __init__(self):
        self.root = Node("Angkor Temples")
        self.category_nodes = {}    # category -> Node
        self.category_members = {}  # category -> [temple names]

    def add_temple_to_category(self, category, temple_name):
        if category not in self.category_nodes:
            self.category_nodes[category] = self.root.add_child(Node(category))
            self.category_members[category] = []
        self.category_nodes[category].add_child(Node(temple_name))
        self.category_members[category].append(temple_name)

    def categories(self):
        return list(self.category_nodes.keys())

    def get_related_temples(self, temple_name):
        for category, members in self.category_members.items():
            if temple_name in members:
                return [name for name in members if name != temple_name]
        return []

    def _print(self, node, level):
        connector = "" if level == 0 else ("    " * (level - 1)) + "|-- "
        print(connector + node.label)
        for child in node.children:
            self._print(child, level + 1)

    def display_all(self):
        print("\n=== All Temples (Root -> Category -> Temple) ===\n")
        self._print(self.root, 0)
        print()

    def display_category(self, category):
        node = self.category_nodes.get(category)
        if node is None:
            print(f"No such category: {category}")
            return
        print(f"\n=== {category} ===\n")
        self._print(node, 0)
        print()