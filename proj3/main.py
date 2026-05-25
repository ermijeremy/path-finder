#!/usr/bin/env python3
from pathlib import Path

from connect_ethio.graph import Graph
from connect_ethio.bfs import bfs_shortest_path
from connect_ethio.dfs import dfs_find_path
from connect_ethio.visualize import draw_network

DATA_FILE = Path(__file__).parent / "data" / "network.txt"
OUTPUT_IMAGE = Path(__file__).parent / "output" / "connect_ethio_paths.png"


def separator(title: str) -> None:
    width = 50
    print(f"\n{'─' * width}")
    print(f"  {title}")
    print(f"{'─' * width}")


def format_path(path: list[str] | None) -> str:
    if path is None:
        return "  ✗  No path found."
    arrows = " → ".join(path)
    return f"  {arrows}\n  Distance: {len(path) - 1} edge(s)"


def show_menu() -> None:
    print("\n╔══════════════════════════════════════════╗")
    print("║      Connect-Ethio Pathfinder Menu       ║")
    print("╠══════════════════════════════════════════╣")
    print("║  1. Display Adjacency List               ║")
    print("║  2. BFS — Find Shortest Path             ║")
    print("║  3. DFS — Find a Valid Path               ║")
    print("║  4. Compare BFS & DFS Paths              ║")
    print("║  5. Remove a User (Edge Case)            ║")
    print("║  6. Visualize the Network                ║")
    print("║  7. Exit                                 ║")
    print("╚══════════════════════════════════════════╝")


def ask_endpoints(graph: Graph) -> tuple[str, str] | None:
    """Prompt the user for source and target, validating they exist."""
    print(f"\n  Available users: {', '.join(graph.nodes())}")
    source = input("  Enter source user: ").strip()
    target = input("  Enter target user: ").strip()

    if not graph.has_node(source):
        print(f"  ✗  '{source}' does not exist in the network.")
        return None
    if not graph.has_node(target):
        print(f"  ✗  '{target}' does not exist in the network.")
        return None
    return source, target


def main() -> None:
    # Load graph once at startup
    graph = Graph.from_file(DATA_FILE)
    print(f"\n  Network loaded from: {DATA_FILE}")
    print(f"  {graph}")

    while True:
        show_menu()
        choice = input("\n  Enter your choice (1-7): ").strip()

        # 1 — Display adjacency list
        if choice == "1":
            separator("Adjacency List")
            graph.display()

        # 2 — BFS shortest path
        elif choice == "2":
            separator("BFS — Shortest Path")
            endpoints = ask_endpoints(graph)
            if endpoints:
                source, target = endpoints
                path = bfs_shortest_path(graph, source, target)
                print(format_path(path))

        # 3 — DFS valid path
        elif choice == "3":
            separator("DFS — Find a Valid Path")
            endpoints = ask_endpoints(graph)
            if endpoints:
                source, target = endpoints
                path = dfs_find_path(graph, source, target)
                print(format_path(path))

        # 4 — Compare BFS & DFS
        elif choice == "4":
            separator("Compare BFS & DFS")
            endpoints = ask_endpoints(graph)
            if endpoints:
                source, target = endpoints
                bfs_path = bfs_shortest_path(graph, source, target)
                dfs_path = dfs_find_path(graph, source, target)

                print(f"\n  BFS result:")
                print(format_path(bfs_path))
                print(f"\n  DFS result:")
                print(format_path(dfs_path))

                if bfs_path and dfs_path:
                    print(f"\n  BFS path length : {len(bfs_path) - 1} edges")
                    print(f"  DFS path length : {len(dfs_path) - 1} edges")
                    if len(bfs_path) <= len(dfs_path):
                        print("  ✓  BFS found the shortest (or equally short) path.")
                    if len(dfs_path) > len(bfs_path):
                        print("  ⚠  DFS path is longer — expected, since DFS does")
                        print("     not guarantee shortest path.")

        # 5 — Remove a user
        elif choice == "5":
            separator("Remove a User (Edge Case)")
            print(f"\n  Available users: {', '.join(graph.nodes())}")
            user = input("  Enter user to remove: ").strip()
            if graph.has_node(user):
                graph.remove_node(user)
                print(f"  ✓  '{user}' has been removed from the network.")
                print(f"  {graph}")
            else:
                print(f"  ✗  '{user}' does not exist in the network.")

        # 6 — Visualize
        elif choice == "6":
            separator("Visualization")
            OUTPUT_IMAGE.parent.mkdir(parents=True, exist_ok=True)

            # Ask if user wants to highlight a path
            print("  Generate with highlighted paths?")
            print("    a) Plain network only")
            print("    b) With BFS & DFS paths (requires source & target)")
            sub = input("  Enter a or b: ").strip().lower()

            if sub == "b":
                endpoints = ask_endpoints(graph)
                if endpoints:
                    source, target = endpoints
                    bfs_path = bfs_shortest_path(graph, source, target)
                    dfs_path = dfs_find_path(graph, source, target)
                    draw_network(graph, bfs_path=bfs_path, dfs_path=dfs_path,
                                 save_path=OUTPUT_IMAGE)
                else:
                    draw_network(graph, save_path=OUTPUT_IMAGE)
            else:
                draw_network(graph, save_path=OUTPUT_IMAGE)

        # 7 — Exit
        elif choice == "7":
            print("\n  Goodbye! 👋\n")
            break

        else:
            print("  ✗  Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
