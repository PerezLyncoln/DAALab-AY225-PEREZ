# NetPATHfinder
### Point-to-Point Shortest Path Analyzer

A single-file, browser-based network visualization and shortest-path tool. Load any edge dataset from an Excel or CSV file, explore the graph interactively, and compute optimal routes between any two nodes across three weighted criteria: **Distance**, **Time**, and **Fuel**.

---

## Table of Contents

1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Input File Format](#input-file-format)
4. [Features](#features)
   - [Graph Visualization](#graph-visualization)
   - [Node Interaction](#node-interaction)
   - [Shortest Path Analysis](#shortest-path-analysis)
   - [Results Panel](#results-panel)
5. [Toolbar Reference](#toolbar-reference)
6. [How the Algorithm Works](#how-the-algorithm-works)
7. [File Structure](#file-structure)
8. [Known Limitations](#known-limitations)

---

## Overview

NetPATHfinder takes a weighted, undirected network (nodes connected by edges with distance, time, and fuel values) and provides two main capabilities:

- **Node Map** — an interactive canvas graph showing all nodes and their connections with live hover and click inspection.
- **Shortest Path** — Dijkstra's algorithm finds the optimal route between any two nodes, optimized for whichever metric you choose, with full breakdowns of all three metrics and alternative routes.

No server, no installation, no dependencies to install. Everything runs locally in the browser from a single `.html` file.

---

## Getting Started

1. Open `MidtermLab2-PEREZ.html` in any modern web browser (Chrome, Firefox, Edge, Safari).
2. Click the upload zone or drag-and-drop your `.xlsx`, `.xls`, or `.csv` file.
3. The graph renders immediately. Use the toolbar and controls to explore.

> **Note:** The XLSX parsing library (`xlsx.js`) is loaded from a CDN. An internet connection is required on first load to fetch that script. Everything else runs offline.

---

## Input File Format

The program expects a spreadsheet or CSV with **5 columns** in this exact order:

| Column | Header (optional) | Description |
|--------|-------------------|-------------|
| 1 | From | Source node ID (number or text) |
| 2 | To | Destination node ID (number or text) |
| 3 | Distance | Edge weight in **kilometers** |
| 4 | Time | Edge weight in **minutes** |
| 5 | Fuel | Edge weight in **liters** |

**Rules:**
- A header row is optional — the parser auto-detects it.
- Each row defines one undirected edge. The program treats every edge as bidirectional (A → B implies B → A).
- If the same pair appears twice (e.g. both `1→2` and `2→1`), the duplicate is deduplicated and only one connection is shown per neighbor.
- Rows with missing or non-numeric values in columns 3–5 are skipped silently.

**Example (CSV):**
```
From,To,Distance,Time,Fuel
1,2,10,15,1.2
1,3,8,20,1.0
2,4,15,30,1.8
2,5,20,35,2.4
3,5,10,20,1.2
4,6,18,35,2.2
5,7,14,28,1.7
6,8,20,40,2.5
7,8,10,18,1.3
```

---

## Features

### Graph Visualization

The network is drawn on an HTML5 Canvas using a **circular layout** — nodes are evenly spaced on a circle. The canvas redraws at up to 60 fps via `requestAnimationFrame`.

**Visual encoding:**
- **Gold node** — selected Start node
- **Cyan-bordered node** — selected End node
- **Cyan path** — the currently active shortest-path or alternative route
- **Dim nodes/edges** — unrelated to the current focus or path
- **Dashed gold ring** — a pinned node
- **Pulsing glow** — animated highlight on hovered/pinned nodes and their connections

**Edge labels** show the current metric value (distance, time, or fuel) at the midpoint of each edge. Labels for all three metrics are shown simultaneously in focus/hover mode.

---

### Node Interaction

#### Hover
Move your mouse over any node to enter **focus mode**:
- All edges and nodes not connected to that node fade out.
- Connected edges glow cyan with directional arrows and full metric labels.
- Neighboring nodes get a soft halo.
- A **floating tooltip** appears showing every unique neighbor with all three metric values.

#### Click (Pin)
Click a node to **pin** it — the focus state locks in place even when you move the mouse away.
- A gold dashed ring and a `📌 PINNED` tag appear on the pinned node.
- The tooltip stays visible showing the pinned node's connections.
- Click the same node again, or click **✕ Unpin** in the toolbar, to release the pin.
- Clicking canvas empty space while pinned does not auto-unpin (use the toolbar button).

#### On New Dataset Load
Loading a new file completely resets all interaction state: the pin is released, the tooltip is hidden, the old graph is cleared immediately, and the results panel is hidden.

---

### Shortest Path Analysis

Use the controls above the graph to configure a path query:

| Control | Description |
|---------|-------------|
| **From Node** | Starting node for the path |
| **To Node** | Destination node |
| **Optimize By** | The metric to minimize: Distance, Time, or Fuel |
| **Find Shortest Path** | Runs the analysis and scrolls to results |

Selecting the same node for both From and To shows a validation error. If no path exists between the two nodes, a "No Path Found" card is shown.

---

### Results Panel

After running a path query, the results section appears with:

#### Path Chain
A visual step-by-step sequence of all nodes in the optimal route:
`[START] → [Node X] → [Node Y] → [END]`

#### Summary Stats
Three metric cards showing the **total** distance, time, and fuel for the found path. The optimized metric is marked with a `★ OPTIMIZED` badge.

#### Optimal Paths for Other Metrics
Two additional panels showing what the path would look like if optimized for the other two metrics instead. Useful for comparing trade-offs (e.g. the fastest route may not be the most fuel-efficient).

#### Alternative Routes
Up to 5 alternative routes ranked by the selected metric. Hovering an alternative route highlights it on the graph in real time, replacing the primary path visualization temporarily.

---

## Toolbar Reference

| Button | Function |
|--------|----------|
| **All Edges** | Show the full network on the graph |
| **Path Only** | Show only nodes and edges on the current path |
| **📏 Dist** | Toggle distance labels on edges |
| **⚡ Time** | Toggle time labels on edges |
| **⛽ Fuel** | Toggle fuel labels on edges |
| **✕ Unpin** | Release the currently pinned node (visible only when a node is pinned) |

---

## How the Algorithm Works

### Dijkstra's Algorithm
The shortest path is found using **Dijkstra's algorithm** — a greedy, priority-queue-based approach guaranteed to find the globally optimal path in a non-negative weighted graph.

For each query:
1. All node distances are initialized to `Infinity`, except the source which is set to `0`.
2. The unvisited node with the smallest tentative distance is selected at each step.
3. Its neighbors' distances are relaxed if a shorter path through the current node is found.
4. The process repeats until the destination is reached or all reachable nodes are exhausted.
5. The path is reconstructed by backtracking through the `prev` map.

The algorithm runs three times per query (once per metric) to populate the "Optimal for Other Metrics" comparison panels.

**Time complexity:** O(V²) with the current array-scan priority queue, where V is the number of nodes. Suitable for graphs up to several hundred nodes.

### Alternative Paths (BFS)
Alternative routes are found using a **BFS-based all-simple-paths** search, capped at 80 candidates to avoid exponential blowup on dense graphs. Results are sorted by the selected metric cost.

---

## File Structure

The entire program is self-contained in a single HTML file:

```
MidtermLab1-PEREZ-v2.html
│
├── <style>          CSS — layout, colors, components, animations
│
├── <body>
│   ├── Header       Title, status bar (node/edge count, state)
│   ├── Upload Zone  Drag-and-drop / click-to-browse file input
│   ├── Controls     From/To node selects, Optimize By, Find button
│   ├── Data Table   Preview of all loaded edges
│   ├── Graph        Toolbar + Canvas + overlay hint
│   └── Results      Path chain, stats, alt metrics, alt routes
│
└── <script>
    ├── State         Global variables (edges, nodes, camera, flags)
    ├── Upload/Parse  FileReader → XLSX → edge array
    ├── initUI()      Resets state, populates UI, starts render loop
    ├── Toolbar       setMode(), toggleLabel(), clearPin()
    ├── Positions     computePositions() — circular layout
    ├── Events        setupEvents() — mouse interactions (runs once)
    ├── Tooltip       updateTooltip() — floating node info card
    ├── Render Loop   requestAnimationFrame + glowPhase animation
    ├── dijkstra()    Weighted shortest path
    ├── allPaths()    BFS alternative routes
    ├── runPathfinder() Orchestrates query + renders results
    └── draw()        Full canvas render (5 passes: ghost edges,
                      focus edges, path edges, nodes, legend)
```

---

## Known Limitations

- **No persistent state** — refreshing the page clears everything. There is no save/load for path results.
- **Undirected only** — all edges are treated as bidirectional. Directed graphs (one-way edges) are not supported.
- **Single path query** — only one From/To pair can be analyzed at a time.
- **Dense graphs** — the all-paths BFS caps at 80 results; very large or dense graphs may not enumerate all alternatives.
- **CDN dependency** — the XLSX parsing library requires an internet connection on first load.
- **No touch support** — canvas interactions (hover, click) are mouse-only; touch/mobile devices are not fully supported.
