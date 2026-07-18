"""
main.py
Terminal interface for the temple search and route navigator.

Data structures used:
  - Hash table  -> instant temple lookup by name
  - Tree        -> temple categories and recommended related temples
  - Graph       -> weighted distances between temples
  - Dijkstra    -> shortest route between two temples
"""

from temple_data import build_hash_table, build_category_tree, build_graph, TEMPLES

AVERAGE_SPEED_KMH = 20  # assumed tuk-tuk / shuttle speed within the park


def print_divider():
    print("-" * 50)


def list_all_temples():
    print_divider()
    print("All temples:")
    for i, temple in enumerate(TEMPLES, start=1):
        print(f"  {i:2}. {temple.name}  ({temple.category})")
    print_divider()


def search_temple(hash_table, tree):
    name = input("Enter a temple name to search: ").strip()
    temple = hash_table.get(name)

    print_divider()
    if temple is None:
        print(f"No temple found matching '{name}'.")
        print_divider()
        return

    print(temple)

    related = tree.get_related_temples(temple.name)
    if related:
        print(f"  Recommended (same category - {temple.category}):")
        for related_name in related:
            print(f"    - {related_name}")
    else:
        print("  No other temples in this category.")
    print_divider()


def find_route(hash_table, graph):
    start_name = input("Enter your current temple: ").strip()
    end_name = input("Enter your destination temple: ").strip()

    print_divider()
    start_temple = hash_table.get(start_name)
    end_temple = hash_table.get(end_name)

    if start_temple is None or end_temple is None:
        missing = start_name if start_temple is None else end_name
        print(f"'{missing}' was not found. Check the spelling and try again.")
        print_divider()
        return

    path, total_distance = graph.dijkstra(start_temple.name, end_temple.name)

    if path is None:
        print(f"No route found between {start_temple.name} and {end_temple.name}.")
        print_divider()
        return

    estimated_minutes = (total_distance / AVERAGE_SPEED_KMH) * 60

    print(f"Shortest route from {start_temple.name} to {end_temple.name}:")
    print("  " + " -> ".join(path))
    print(f"  Total distance     : {total_distance:.1f} km")
    print(f"  Estimated travel   : {estimated_minutes:.0f} minutes "
          f"(at ~{AVERAGE_SPEED_KMH} km/h)")
    print_divider()


def main():
    hash_table = build_hash_table()
    tree = build_category_tree()
    graph = build_graph()

    menu = (
        "\nTemple navigator\n"
        "  1. Search for a temple\n"
        "  2. Find shortest route between two temples\n"
        "  3. List all temples\n"
        "  4. Exit\n"
    )

    while True:
        print(menu)
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            search_temple(hash_table, tree)
        elif choice == "2":
            find_route(hash_table, graph)
        elif choice == "3":
            list_all_temples()
        elif choice == "4":
            print("Goodbye.")
            break
        else:
            print("Invalid option. Please choose 1-4.")


if __name__ == "__main__":
    main()