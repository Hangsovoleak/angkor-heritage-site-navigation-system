# """
# tree.py
# A tree structure that organizes temples by category, so that once a temple
# is found, related/recommended temples in the same category can be surfaced.
# """


# class TreeNode:
#     def __init__(self, name):
#         self.name = name
#         self.temples = []       # temple names that belong directly to this category
#         self.children = []      # sub-category TreeNodes (not required for 15 temples,
#                                  # but supports deeper grouping if the dataset grows)

#     def add_temple(self, temple_name):
#         self.temples.append(temple_name)

#     def add_child(self, child_node):
#         self.children.append(child_node)


# class CategoryTree:
#     def __init__(self):
#         self.root = TreeNode("All temples")
#         self.category_nodes = {}

#     def add_category(self, category_name):
#         if category_name in self.category_nodes:
#             return self.category_nodes[category_name]
#         node = TreeNode(category_name)
#         self.root.add_child(node)
#         self.category_nodes[category_name] = node
#         return node

#     def add_temple_to_category(self, category_name, temple_name):
#         node = self.add_category(category_name)
#         node.add_temple(temple_name)

#     def get_category_of(self, temple_name):
#         for category_name, node in self.category_nodes.items():
#             if temple_name in node.temples:
#                 return category_name
#         return None

#     def get_related_temples(self, temple_name, limit=3):
#         """Return up to `limit` other temples that share this temple's category."""
#         category_name = self.get_category_of(temple_name)
#         if not category_name:
#             return []
#         node = self.category_nodes[category_name]
#         related = [t for t in node.temples if t != temple_name]
#         return related[:limit]

#     def print_tree(self):
#         print(self.root.name)
#         for category_node in self.root.children:
#             print(f"  |-- {category_node.name}")
#             for temple_name in category_node.temples:
#                 print(f"        - {temple_name}")




# new code


# --- Category tree (from tree.py) ---
class TreeNode:
    def __init__(self, name):
        self.name = name
        self.temples = []
        self.children = []

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


# --- Distance tree (binary tree) ---
class Node:
    def __init__(self, name, distance, left=None, right=None):
        self.name = name
        self.distance = distance
        self.left = left
        self.right = right


# Renamed to avoid clashing with CategoryTree's print method
def print_distance_tree(node, level=0, prefix="Root: "):
    if node is not None:
        print(" " * (level * 4) + prefix + f"{node.name} ({node.distance})")
        if node.left or node.right:
            print_distance_tree(node.left, level + 1, "L--- ")
            print_distance_tree(node.right, level + 1, "R--- ")


# --- Execution Block ---
if __name__ == "__main__":
    # --- Build the distance tree ---
    root = Node("Angkor Wat", "0 km")
    root.left = Node("Phnom Bakheng", "1.3 km")
    root.right = Node("Bayon", "3.5 km")
    root.left.left = Node("Baphoun", "4 km")
    root.left.right = Node("Chau say", "6 km")
    root.right.left = Node("Thmmanon", "6 km")
    root.right.right = Node("Takeo", "6.5 km")
    root.left.left.left = Node("Tapromh", "7 km")
    root.left.left.right = Node("Banteay Kdei", "7.5 km")
    root.left.right.left = Node("Preah Khan", "8.5 km")
    root.left.right.right = Node("Neak Poan", "11.5 km")
    root.right.left.left = Node("Pre rub", "13 km")
    root.right.left.right = Node("Ta som", "14 km")
    root.right.right.left = Node("East Mebon", "14.5 km")
    root.right.right.right = Node("Banteay Srei", "32 km")

    # --- Build the category tree ---
    categories = CategoryTree()
    categories.add_temple_to_category("Hindu", "Angkor Wat")
    categories.add_temple_to_category("Hindu", "Banteay Srei")
    categories.add_temple_to_category("Buddhist", "Bayon")
    categories.add_temple_to_category("Buddhist", "Phnom Bakheng")
    categories.add_temple_to_category("Buddhist", "Takeo")
    categories.add_temple_to_category("Buddhist", "Thmmanon")
    categories.add_temple_to_category("Jungle", "Tapromh")
    categories.add_temple_to_category("Jungle", "Preah Khan")
    categories.add_temple_to_category("Jungle", "Neak Poan")
    categories.add_temple_to_category("Jungle", "Ta som")
    categories.add_temple_to_category("Terrace", "Baphoun")
    categories.add_temple_to_category("Terrace", "Chau say")
    categories.add_temple_to_category("Terrace", "East Mebon")
    categories.add_temple_to_category("Terrace", "Banteay Kdei")
    categories.add_temple_to_category("Terrace", "Pre rub")

    # --- Demo ---
    print("--- Distance Tree Structure ---")
    print_distance_tree(root)

    print("\n--- Category Tree Structure ---")
    categories.print_tree()

    print("\n--- Example: viewing 'Bayon' ---")
    print(f"Category: {categories.get_category_of('Bayon')}")
    print(f"Related temples (same category): {categories.get_related_temples('Bayon')}")