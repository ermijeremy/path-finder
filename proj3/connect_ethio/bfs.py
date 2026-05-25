from __future__ import annotations
from collections import deque
from typing import List, Optional

from .graph import Graph


def bfs_shortest_path(
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

    visited: set[str] = {source}    # an array to store the visted nodes
    queue: deque[list[str]] = deque([[source]]) # a queue to store the path

    while queue:
        path = queue.popleft()
        current = path[-1]
        print("path: ", path)
        print("current: ", current)

        for neighbour in graph.neighbours(current):
            if neighbour == target:
                return path + [neighbour]
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(path + [neighbour])

    # No connection found
    return None
