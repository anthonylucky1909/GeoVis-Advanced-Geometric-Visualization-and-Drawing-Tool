# GeoVis: Advanced Geometric Visualization and Drawing Tool ✨

## Overview 📝

**Compute-Graphic** is a powerful **computational geometry** and **graphical drawing** application designed to help users explore, visualize, and implement a variety of geometric algorithms through a user-friendly graphical interface and a flexible command-line interface (CLI). Built using **Qt** for the graphical user interface (GUI) and **Python** for the application logic, this tool supports drawing geometric shapes, executing geometric algorithms, and visualizing results interactively.

The application is perfect for students, developers, and researchers looking to experiment with common computational geometry algorithms such as **convex hull**, **line intersection**, and **polygon clipping**, or for anyone needing a flexible graphical tool for drawing and analyzing geometric shapes. 🔍

## Key Features ⚡

### **Interactive Graphical User Interface (GUI)** 🖥️
- **Dynamic Shape Drawing**: Easily draw and manipulate geometric shapes like circles, polygons, and lines using the Qt-based GUI. 🎨
- **Real-Time Algorithm Visualization**: Visualize the step-by-step execution of algorithms, such as convex hull construction, Voronoi diagrams, or line intersection problems, directly on the canvas. 🔄
- **Interactive Shapes**: Click and drag to move shapes, adjust their size, or reposition them for custom geometry exploration. 🖱️
- **Zoom and Pan**: Zoom in and out of the canvas for detailed views of the shapes and algorithms in action. Pan across the canvas to explore large drawings. 🔍

### **Algorithm Support** ⚙️
- **Convex Hull Algorithms**: Visualize popular convex hull algorithms such as **Graham Scan** and **QuickHull**, showing intermediate steps and the final hull construction. 🏔️
- **Line Intersection**: Detect and highlight the intersection points of two or more geometric objects (e.g., lines, segments). ✂️
- **Polygon Clipping**: Clip polygons based on various geometric operations like intersection, difference, and union, and visualize the resulting shapes. 🔲
- **Voronoi Diagrams**: Generate and visualize Voronoi diagrams based on a set of points, showing how the plane is partitioned based on proximity. 📐
- **Geometric Transformations**: Apply transformations such as rotation, scaling, and translation to geometric objects, and see how they affect the overall layout. 🔄

### **Command-Line Interface (CLI)** ⌨️
- **Automated Drawing**: Use a simple and concise CLI to generate drawings and compute geometric properties from pre-defined input configurations. 📝
- **Batch Processing**: Execute multiple drawing and algorithm operations in a sequence through the CLI, allowing for batch processing of geometry tasks. ⚙️
- **Algorithm Execution**: Run algorithms directly via the CLI without launching the GUI, useful for automated testing or running large-scale computations. 🚀

### **File Input/Output Support** 💾
- **Input from Text Files**: Define shapes, algorithms, and parameters in an external `input.txt` file, allowing users to easily load predefined configurations on application startup. 📂
- **Export Visualizations**: Save the graphical output as images or vector files (e.g., PNG, SVG) to share or use in documentation. 🖼️

## Files and Project Structure 🗂️

The **Compute-Graphic** application consists of several Python scripts and supporting files for the backend algorithms, graphical user interface, and input/output handling.

### **Core Application Logic** 🧠
- **`cg_algorithms.py`**: Contains the primary computational geometry algorithms implemented in Python. This file includes algorithms for drawing geometric shapes, performing geometric transformations, and running common geometric algorithms (e.g., convex hull, line intersection).
    - **Convex Hull Algorithms**: `graham_scan()`, `quick_hull()`
    - **Line Intersection**: `line_intersection()`
    - **Polygon Clipping**: `clip_polygon()`
    - **Voronoi Diagram**: `generate_voronoi()`

- **`cg_cli.py`**: Command-line interface script for interacting with the application. This file processes user commands, interprets the input for geometric operations, and runs the corresponding algorithms.
    - **Commands**: `draw_circle`, `draw_polygon`, `calculate_hull`, `generate_voronoi`
    - **Batch Commands**: Execute a series of commands by chaining them in a script or command sequence.

- **`cg_gui.py`**: The graphical user interface script built with **PyQt5**. It provides the canvas where users can interact with shapes, apply transformations, and visualize algorithms. The GUI also provides interactive buttons, sliders, and status bars to manage the application state.
    - **Canvas Interaction**: Click and drag for shape manipulation, zooming, and panning.
    - **Algorithm Visualization**: Displays step-by-step execution of selected algorithms.

### **Supporting Files** 🗒️
- **`input.txt`**: A plain text file that contains predefined shapes, commands, or configurations that are loaded automatically when the application starts. Users can define shapes to be drawn, algorithm operations, and other initialization settings.
    - Example:
      ```txt
      circle 100 100 50
      rectangle 150 150 100 50
      convex_hull 10 20 30 40 50
      ```

- **`README.md`**: This file, containing detailed documentation, setup instructions, and usage guidelines.

- **`Compute-Graphic.pro`**: Qt project file used for building the application using the **Qt Creator** IDE. It contains configuration settings for the GUI and links to necessary Qt modules.

- **`LICENSE`**: Contains licensing information for the project (e.g., MIT License).

### **Project Metadata and Dependencies** 📦
- **Python 3.x**: Required for running the core logic and algorithms.
- **PyQt5**: A Python binding for Qt, used to build the graphical user interface.
    - Install with:
      ```bash
      pip install PyQt5
      ```

## Setup Instructions ⚙️

### Prerequisites 🛠️
Before running the application, ensure you have the following installed:

- **Python** 3.x or higher.
- **PyQt5** for the GUI:
  ```bash
  pip install PyQt5
