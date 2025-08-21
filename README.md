# LiteDraw: Geometry Drawing App ✨

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)  
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)  
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15.9-41CD52.svg)](https://pypi.org/project/PyQt5/)

## 📖 Overview

**LiteDraw** (formerly **GeoVis**) is a lightweight application for **geometry drawing and visualization**, built with **Python** and **Qt (PyQt5)**.  

It supports both an **interactive graphical interface** and a **command-line interface (CLI)**, enabling users to draw shapes, execute geometric algorithms, and visualize results step by step.

---

## 🚀 Features

### Graphical Interface (GUI)
- Draw and manipulate **circles, lines, and polygons**  
- Interactive canvas with **zoom and pan**  
- Step-by-step visualization of algorithms:
  - Convex Hull (Graham Scan, QuickHull)  
  - Line Intersection  
  - Polygon Clipping  
  - Voronoi Diagram (basic)  

### Command-Line Interface (CLI)
- Execute geometry commands directly:
  ```txt
  draw_circle 100 100 50
  convex_hull 10 20 30 40 50
  ```
- Process batch commands from `input.txt`  

### File Support
- Import shapes and algorithm configs from `input.txt`  
- Export visualizations to **PNG** or **SVG**  

---

## 📁 Project Structure

| File | Description |
|------|-------------|
| `cg_algorithms.py` | Core computational geometry algorithms |
| `cg_gui.py` | PyQt5-based GUI application |
| `cg_cli.py` | CLI for batch processing |
| `input.txt` | Example commands file |
| `Compute-Graphic.pro` | Qt Creator project configuration |
| `README.md` | Project documentation |
| `LICENSE` | License file |

---

## ⚙️ Requirements

- Python **3.8+**  
- PyQt5 → install with:
  ```bash
  pip install PyQt5
  ```

---

## 💡 Example Input (`input.txt`)

```txt
circle 100 100 50
rectangle 150 150 100 50
convex_hull 10 20 30 40 50
```

---

## 🏃 Usage

### Run GUI
```bash
python cg_gui.py
```

### Run CLI
```bash
python cg_cli.py input.txt
```

---

## 🛠️ Development

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/litedraw.git
cd litedraw
pip install -r requirements.txt
```

Run in development mode:

```bash
python cg_gui.py
```

Contributions are welcome! Please open issues and submit pull requests.

---

## 📜 License

This project is licensed under the [Apache 2.0 License](LICENSE).
