# LiteDraw: Geometry Drawing App ✨

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15.9-41CD52.svg)](https://pypi.org/project/PyQt5/)

## Overview

**GeoVis** is a lightweight **geometry drawing and visualization** tool built using **Python** and **Qt**.  
It lets users draw shapes, run geometric algorithms (like convex hull and line intersection), and view results interactively via **GUI** or **CLI**.

---

## 🚀 Features

### 🖥️ Graphical Interface (GUI)

- Draw and move circles, lines, and polygons
- Zoom and pan on canvas
- Step-by-step visualization of algorithms like:
  - Convex Hull (Graham Scan, QuickHull)
  - Line Intersection
  - Polygon Clipping
  - Voronoi Diagram

### ⌨️ Command-Line Interface (CLI)

- Run geometry commands like `draw_circle`, `calculate_hull`
- Process batch commands from `input.txt`

### 💾 File Support

- Read shape and algorithm configs from `input.txt`
- Export visualizations to images (e.g., PNG, SVG)

---

## 📁 File Structure

| File | Description |
|------|-------------|
| `cg_algorithms.py` | Geometry algorithms (convex hull, intersection, etc.) |
| `cg_gui.py` | PyQt5 GUI application |
| `cg_cli.py` | CLI for running commands |
| `input.txt` | Define shapes and commands for batch processing |
| `Compute-Graphic.pro` | Qt project config for Qt Creator |
| `README.md` | This guide |
| `LICENSE` | License info |

---

## ⚙️ Requirements

- Python 3.x
- PyQt5 (`pip install PyQt5`)

---

## 💡 Example Input File (`input.txt`)

```txt
circle 100 100 50
rectangle 150 150 100 50
convex_hull 10 20 30 40 50
