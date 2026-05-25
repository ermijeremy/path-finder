from __future__ import annotations
from typing import List, Optional, Set

from .graph import Graph


def dfs_find_path(
    graph: Graph,
    source: str,
    target: str,
) -> Optional[List[str]]:
    # Edge-cases
    if not graph.has_node(source):
        print(f"Source node '{source}' does not exist in the network.")
        return None
    if not graph.has_node(target):
        print(f"Target node '{target}' does not exist in the network.")
        return None
    if source == target:
        return [source]

    # DFS
    visited: Set[str] = set()    # an array to store the visted nodes
    stack: list[list[str]] = [[source]]   # stores the path 

    while stack:
        path = stack.pop()
        current = path[-1]
        print("path: ", path)
        print("current: ", current)

        if current in visited:
            continue
        visited.add(current)

        if current == target:
            return path

        # last from stack → first to be explored
        for neighbour in reversed(graph.neighbours(current)):
            if neighbour not in visited:
                stack.append(path + [neighbour])

    # No connection found
    return None
