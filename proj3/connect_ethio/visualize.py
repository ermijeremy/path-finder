from __future__ import annotations
from pathlib import Path
from typing import List, Optional

try:
    import matplotlib.pyplot as plt
    import networkx as nx

    HAS_VIZ = True
except ImportError:
    HAS_VIZ = False

from .graph import Graph


# Colour
_NODE_DEFAULT = "#2c3e50"
_NODE_SOURCE = "#27ae60"
_NODE_TARGET = "#e74c3c"
_NODE_ON_PATH = "#f39c12"
_EDGE_DEFAULT = "#95a5a6"
_EDGE_ON_PATH = "#e74c3c"
_LABEL_COLOR = "white"


def _build_nx_graph(graph: Graph) -> "nx.Graph":
    """Convert our Graph to a NetworkX Graph for drawing."""
    G = nx.Graph()
    for node in graph.nodes():
        G.add_node(node)
        for nbr in graph.neighbours(node):
            G.add_edge(node, nbr)
    return G


def draw_network(
    graph: Graph,
    bfs_path: Optional[List[str]] = None,
    dfs_path: Optional[List[str]] = None,
    save_path: Optional[str | Path] = None,
) -> None:
    if not HAS_VIZ:
        print(
            "matplotlib / networkx not installed. "
            "Install with:  pip install matplotlib networkx"
        )
        return

    G = _build_nx_graph(graph)
    pos = nx.spring_layout(G, seed=42, k=1.8)

    num_plots = 1 + bool(bfs_path) + bool(dfs_path)
    fig, axes = plt.subplots(1, num_plots, figsize=(8 * num_plots, 7))
    if num_plots == 1:
        axes = [axes]

    # Helper to draw one subplot
    def _draw(ax, title, path=None):
        ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
        ax.set_facecolor("#f8f9fa")

        # Edge colours
        edge_colors = []
        edge_widths = []
        path_edges = set()
        if path:
            path_edges = {
                (path[i], path[i + 1]) for i in range(len(path) - 1)
            }
            path_edges |= {(v, u) for u, v in path_edges}

        for u, v in G.edges():
            if (u, v) in path_edges:
                edge_colors.append(_EDGE_ON_PATH)
                edge_widths.append(3.0)
            else:
                edge_colors.append(_EDGE_DEFAULT)
                edge_widths.append(1.2)

        # Node colours
        node_colors = []
        path_set = set(path) if path else set()
        for n in G.nodes():
            if path and n == path[0]:
                node_colors.append(_NODE_SOURCE)
            elif path and n == path[-1]:
                node_colors.append(_NODE_TARGET)
            elif n in path_set:
                node_colors.append(_NODE_ON_PATH)
            else:
                node_colors.append(_NODE_DEFAULT)

        nx.draw_networkx_edges(
            G, pos, ax=ax,
            edge_color=edge_colors, width=edge_widths, alpha=0.8,
        )
        nx.draw_networkx_nodes(
            G, pos, ax=ax,
            node_color=node_colors, node_size=700, edgecolors="white",
            linewidths=2,
        )
        nx.draw_networkx_labels(
            G, pos, ax=ax,
            font_size=8, font_weight="bold", font_color=_LABEL_COLOR,
        )

        # Legend text
        if path:
            label = " → ".join(path)
            ax.text(
                0.5, -0.05, f"Path ({len(path)-1} edges): {label}",
                transform=ax.transAxes, ha="center", fontsize=9,
                style="italic", color="#555",
            )

    # Render subplots
    idx = 0
    _draw(axes[idx], "Connect-Ethio Network")
    idx += 1
    if bfs_path:
        _draw(axes[idx], "BFS – Shortest Path", bfs_path)
        idx += 1
    if dfs_path:
        _draw(axes[idx], "DFS – Valid Path", dfs_path)

    plt.tight_layout()
    if save_path:
        fig.savefig(str(save_path), dpi=150, bbox_inches="tight")
        print(f"  ✓  Figure saved → {save_path}")
    else:
        plt.show()
    plt.close(fig)
