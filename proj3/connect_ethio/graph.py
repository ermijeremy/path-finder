from __future__ import annotations
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set


class Graph:
    """Undirected, unweighted graph stored as an adjacency list."""

    def __init__(self) -> None:
        self._adj: Dict[str, List[str]] = defaultdict(list)

    def add_edge(self, u: str, v: str) -> None:
        """Add an undirected edge between users u and v."""
        if v not in self._adj[u]:
            self._adj[u].append(v)
        if u not in self._adj[v]:
            self._adj[v].append(u)

    def remove_node(self, node: str) -> None:
        """Remove a user (node) and all their connections from the network."""
        if node in self._adj:
            for neighbour in self._adj[node]:
                self._adj[neighbour] = [
                    n for n in self._adj[neighbour] if n != node
                ]
            del self._adj[node]

    def neighbours(self, node: str) -> List[str]:
        """Return the sorted neighbour list of node."""
        return sorted(self._adj.get(node, []))

    def nodes(self) -> List[str]:
        """Return all nodes in sorted order."""
        return sorted(self._adj.keys())

    def has_node(self, node: str) -> bool:
        """Check whether node exists in the graph."""
        return node in self._adj

    def edge_count(self) -> int:
        """Return the total number of undirected edges."""
        return sum(len(nbrs) for nbrs in self._adj.values()) // 2

    @classmethod
    def from_file(cls, filepath: str | Path) -> "Graph":
        graph = cls()
        path = Path(filepath)
        with path.open() as fh:
            for line in fh:
                parts = line.strip().split()
                if len(parts) >= 2:
                    graph.add_edge(parts[0], parts[1])
        return graph

    def display(self) -> None:
        """print the adjacency list."""
        print("\n╔══════════════════════════════════════╗")
        print("║       Adjacency List (sorted)        ║")
        print("╠══════════════════════════════════════╣")
        for node in self.nodes():
            nbrs = ", ".join(self.neighbours(node))
            print(f"║  {node:<10} → [{nbrs}]")
        print("╚══════════════════════════════════════╝")

    def __repr__(self) -> str:
        return f"Graph(nodes={len(self.nodes())}, edges={self.edge_count()})"
