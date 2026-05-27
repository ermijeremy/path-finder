# Connect-Ethio — Social Network Pathfinder

A modular Python implementation of BFS and DFS graph-search algorithms applied
to a professional social networking platform.

---

##  Project Structure

```
proj3/
├── connect_ethio/          # Core library package
│   ├── __init__.py         # Public API exports
│   ├── graph.py            # Graph class (adjacency-list representation)
│   ├── bfs.py              # Breadth-First Search implementation
│   ├── dfs.py              # Depth-First Search implementation
│   └── visualize.py        # matplotlib / networkx visualization helpers
├── data/
│   └── network.txt         # Edge list of the sample network
├── output/
│   └── connect_ethio_paths.png   # Generated visualization (after running)
├── main.py                 # Interactive driver with menu system
├── report.md               # Analysis report (deliverables 1–3)
├── requirements.txt        # Python dependencies
└── README.md               # ← you are here
```

##  Setup

```bash
# 1. Create a virtual environment
python3 -m venv .venv && source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt
```


##  Running

```bash
python3 main.py
```

The program presents an interactive menu where you choose a service by number:

```
╔══════════════════════════════════════════╗
║      Connect-Ethio Pathfinder Menu       ║
╠══════════════════════════════════════════╣
║  1. Display Adjacency List               ║
║  2. BFS — Find Shortest Path             ║
║  3. DFS — Find a Valid Path              ║
║  4. Compare BFS & DFS Paths              ║
║  5. Remove a User (Edge Case)            ║
║  6. Visualize the Network                ║
║  7. Exit                                 ║
╚══════════════════════════════════════════╝
```

| Option | What it does | Asks for input? |
|--------|-------------|-----------------|
| **1** | Prints the full adjacency list | No |
| **2** | Runs BFS to find the shortest path | Yes — source & target |
| **3** | Runs DFS to find any valid path | Yes — source & target |
| **4** | Runs both BFS & DFS and compares results | Yes — source & target |
| **5** | Removes a user from the network | Yes — user to remove |
| **6** | Generates a visualization PNG | Optional — source & target for path overlay |
| **7** | Exits the program | No |

---

##  Network Graph

The sample Connect-Ethio network (`data/network.txt`):

```
                          ┌── Akirem
                          │
           ┌── Amanuel ───┼── Dan
           │      │       │
           │  Abdellah ───┼── Adomiyas
           │   │    │     │
           │   │  Aymen   └── Abel ──┐
           │   │                │    │
           │   └────────────────┘    │
           │                         │
  Abel ────┼── Biniam ──┬── Desta ───┼── Zewdu
           │            │      │
           │          Lemlem  Kidst
           │          │    │
           │      Abreham  Atakilt
           │                 │
           └── Kaleab ──┬── Bethy ──┬── Eyob ──┘
                   │    │           │
                 Ephrem Leawi     Atakilt
                 │    │
               Hana  Fasil
```

### Adjacency List

| User      | Connected To                         |
|-----------|--------------------------------------|
| Abdellah  | Abel, Adomiyas, Amanuel, Aymen       |
| Abel      | Abdellah, Amanuel, Biniam, Kaleab    |
| Abreham   | Lemlem                               |
| Adomiyas  | Abdellah                             |
| Akirem    | Amanuel                              |
| Amanuel   | Abdellah, Abel, Akirem, Dan          |
| Atakilt   | Eyob, Lemlem                         |
| Aymen     | Abdellah                             |
| Bethy     | Eyob, Kaleab, Leawi                  |
| Biniam    | Abel, Desta, Lemlem                  |
| Dan       | Amanuel                              |
| Desta     | Biniam, Kidst, Zewdu                 |
| Efrem     | Kaleab                               |
| Ephrem    | Fasil, Hana                          |
| Eyob      | Atakilt, Bethy                       |
| Fasil     | Ephrem                               |
| Hana      | Ephrem                               |
| Kaleab    | Abel, Bethy, Efrem                   |
| Kidst     | Desta                                |
| Leawi     | Bethy                                |
| Lemlem    | Abreham, Atakilt, Biniam             |
| Zewdu     | Desta                                |

**22 users, 22 edges**

##  Sample Output

### Option 1 — Display Adjacency List

```
──────────────────────────────────────────────────
  Adjacency List
──────────────────────────────────────────────────

╔══════════════════════════════════════╗
║       Adjacency List (sorted)        ║
╠══════════════════════════════════════╣
║  Abdellah   → [Abel, Adomiyas, Amanuel, Aymen]
║  Abel       → [Abdellah, Amanuel, Biniam, Kaleab]
║  Abreham    → [Lemlem]
║  ...
╚══════════════════════════════════════╝
```

### Option 2 — BFS (Abel → Zewdu)

```
──────────────────────────────────────────────────
  BFS — Shortest Path
──────────────────────────────────────────────────

  Available users: Abdellah, Abel, Abreham, ...
  Enter source user: Abel
  Enter target user: Zewdu

  Abel → Biniam → Desta → Zewdu
  Distance: 3 edge(s)
```

### Option 3 — DFS (Abel → Zewdu)

```
──────────────────────────────────────────────────
  DFS — Find a Valid Path
──────────────────────────────────────────────────

  Available users: Abdellah, Abel, Abreham, ...
  Enter source user: Abel
  Enter target user: Zewdu

  Abel → Biniam → Desta → Zewdu
  Distance: 3 edge(s)
```

### Option 5 — Remove a User

```
──────────────────────────────────────────────────
  Remove a User (Edge Case)
──────────────────────────────────────────────────

  Available users: Abdellah, Abel, Abreham, ...
  Enter user to remove: Desta
  ✓  'Desta' has been removed from the network.
```

After removal, searching for Abel → Zewdu returns **"No path found"** since
Zewdu is only reachable through Desta.
