"""
tree.py
A tree structure that organizes temples by category, so that once a temple
is found, related/recommended temples in the same category can be surfaced.
"""


class TreeNode:
    def __init__(self, name):
        self.name = name
        self.temples = []       # temple names that belong directly to this category
        self.children = []      # sub-category TreeNodes (not required for 15 temples,
                                 # but supports deeper grouping if the dataset grows)

    def add_temple(self, temple_name):
        self.temples.append(temple_name)

    def add_child(self, child_node):
        self.children.append(child_node)


class CategoryTree:
    def __init__(self):
        self.root = TreeNode("All temples")
        self.category_nodes = {}

    def add_category(self, category_name):
        if category_name in self.category_nodes:
            return self.category_nodes[category_name]
        node = TreeNode(category_name)
        self.root.add_child(node)
        self.category_nodes[category_name] = node
        return node

    def add_temple_to_category(self, category_name, temple_name):
        node = self.add_category(category_name)
        node.add_temple(temple_name)

    def get_category_of(self, temple_name):
        for category_name, node in self.category_nodes.items():
            if temple_name in node.temples:
                return category_name
        return None

    def get_related_temples(self, temple_name, limit=3):
        """Return up to `limit` other temples that share this temple's category."""
        category_name = self.get_category_of(temple_name)
        if not category_name:
            return []
        node = self.category_nodes[category_name]
        related = [t for t in node.temples if t != temple_name]
        return related[:limit]

    def print_tree(self):
        print(self.root.name)
        for category_node in self.root.children:
            print(f"  |-- {category_node.name}")
            for temple_name in category_node.temples:
                print(f"        - {temple_name}")