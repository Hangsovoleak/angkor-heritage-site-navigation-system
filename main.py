"""
main.py
Angkor Temple Travel Guide - a terminal app that helps visitors search
temples, discover nearby sights, and plan routes across the park on
their own, without needing a tour guide.

Under the hood it's built from three fundamental data structures - a
hash table for instant temple lookup, a category tree for
recommendations, and a weighted graph with Dijkstra's algorithm for
route planning - but the traveler using it never needs to know that.
"""

from temple_data import build_hash_table, build_category_tree, build_graph, TEMPLES

AVERAGE_SPEED_KMH = 20  # assumed tuk-tuk / shuttle speed within the park


def print_divider():
    print("-" * 50)


def print_welcome():
    print("=" * 50)
    print(" ANGKOR TEMPLE TRAVEL GUIDE")
    print(" Explore 15 temples across the park on your own.")
    print("=" * 50)


def show_temple_list():
    print_divider()
    print("Temple list (search by name or by its number):")
    for temple in TEMPLES:
        print("  " + temple.short())
    print_divider()


def find_temple(directory, recommendations):
    query = input("\nWhich temple are you looking for? (name or number): ").strip()
    temple = directory.get(query)

    print_divider()
    if temple is None:
        print(f"Sorry, no temple matches '{query}'. Try the name or its number "
              "from the temple list (option 4).")
        print_divider()
        return

    print(temple)
    print_divider()

    nearby = recommendations.get_related_temples(temple.name)
    if not nearby:
        print("No other temples share this category nearby.")
        print_divider()
        return

    print(f"You might also enjoy these {len(nearby)} temple(s) nearby, "
          f"in the same category ({temple.category}):")
    for name in nearby:
        print(f"  - {name}")

    offer_nearby_temples(directory, nearby)


def offer_nearby_temples(directory, nearby_names):
    """Let the traveler flip through nearby temples one at a time, if they want to."""
    for name in nearby_names:
        answer = input("\nWant to see details for the next one? (y/n): ").strip().lower()
        if answer != "y":
            break
        print_divider()
        print(directory.get(name))
    print_divider()


def plan_route(directory, route_planner):
    start_query = input("\nWhere are you now? (temple name or number): ").strip()
    end_query = input("Where do you want to go? (temple name or number): ").strip()

    print_divider()
    start_temple = directory.get(start_query)
    end_temple = directory.get(end_query)

    if start_temple is None or end_temple is None:
        missing = start_query if start_temple is None else end_query
        print(f"Couldn't find '{missing}'. Check the spelling or number and try again.")
        print_divider()
        return

    path, total_distance = route_planner.dijkstra(start_temple.name, end_temple.name)

    if path is None:
        print(f"No known route between {start_temple.name} and {end_temple.name}.")
        print_divider()
        return

    estimated_minutes = (total_distance / AVERAGE_SPEED_KMH) * 60

    print(f"Best route from {start_temple.name} to {end_temple.name}:")
    print("  " + " -> ".join(path))
    print(f"  Distance          : {total_distance:.1f} km")
    print(f"  Estimated travel  : {estimated_minutes:.0f} minutes "
          f"(at ~{AVERAGE_SPEED_KMH} km/h)")
    print_divider()


def explore_by_type(recommendations):
    categories = recommendations.categories()

    print_divider()
    print("What type of temple do you want to explore?")
    print("1. All temples")
    for i, category in enumerate(categories, start=2):
        print(f"{i}. {category}")
    print_divider()

    choice = input("Choose an option: ").strip()

    if choice == "1":
        recommendations.display_all()
        return

    try:
        index = int(choice) - 2
        if 0 <= index < len(categories):
            recommendations.display_category(categories[index])
            return
    except ValueError:
        pass

    print("Invalid option.")


def main():
    directory = build_hash_table()            # instant temple lookup
    recommendations = build_category_tree()    # categories & "you might also like"
    route_planner = build_graph()              # distances + shortest-route planning

    print_welcome()

    menu = (
        "\nWhat would you like to do?\n"
        "  1. Find a temple\n"
        "  2. Plan a route between two temples\n"
        "  3. Explore temples by type\n"
        "  4. See the full temple list\n"
        "  5. Exit\n"
    )

    while True:
        print(menu)
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            find_temple(directory, recommendations)
        elif choice == "2":
            plan_route(directory, route_planner)
        elif choice == "3":
            explore_by_type(recommendations)
        elif choice == "4":
            show_temple_list()
        elif choice == "5":
            print("Safe travels!")
            break
        else:
            print("Please choose an option between 1 and 5.")


if __name__ == "__main__":
    main()