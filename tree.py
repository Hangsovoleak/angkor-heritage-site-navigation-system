class Node:
    def __init__(self, name, distance, left=None, right=None):
        self.name = name
        self.distance = distance
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Node({self.name}, {self.distance})"


# --- Level 0 (Root) ---
root = Node("Angkor Wat", "0 km")

# --- Level 1 ---
root.left = Node("Phnom Bakheng", "1.3 km")
root.right = Node("Bayon", "3.5 km")

# --- Level 2 ---
root.left.left = Node("Baphoun", "4 km")
root.left.right = Node("Chau say", "6 km")

root.right.left = Node("Thmmanon", "6 km")
root.right.right = Node("Takeo", "6.5 km")

# --- Level 3 (Leaves) ---
root.left.left.left = Node("Tapromh", "7 km")
root.left.left.right = Node("Banteay Kdei", "7.5 km")

root.left.right.left = Node("Preah Khan", "8.5 km")
root.left.right.right = Node("Neak Poan", "11.5 km")

root.right.left.left = Node("Pre rub", "13 km")
root.right.left.right = Node("Ta som", "14 km")

root.right.right.left = Node("East Mebon", "14.5 km")
root.right.right.right = Node("Banteay Srei", "32 km")

def print_tree(node, level=0, prefix="Root: "):
    if node is not None:
        print(" " * (level * 4) + prefix + f"{node.name} ({node.distance})")
        if node.left or node.right:
            print_tree(node.left, level + 1, "L--- ")
            print_tree(node.right, level + 1, "R--- ")

print("--- Generated Angkor Tree Structure ---")
print_tree(root)