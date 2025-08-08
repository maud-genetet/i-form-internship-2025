# I-Form

Application for analyzing finite element analysis results.

# Table of Contents
- [Features](#features)
  - [Main Features](#main-features)
  - [Analysis Tools](#analysis-tools)
- [Technical Features](#technical-features)
- [Prerequisites](#prerequisites)
  - [System Configuration](#system-configuration)
  - [Dependencies](#dependencies)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage Guide](#usage-guide)
  - [Getting Started](#getting-started)
  - [Main Features](#main-features-1)
    - [Animation Controls](#animation-controls)
    - [3D Model Generation](#3d-model-generation)
    - [Interactive Analysis](#interactive-analysis)
    - [Graphics and Plotting](#graphics-and-plotting)
    - [Camera Recalibration](#camera-recalibration)
  - [Visualization Options](#visualization-options)
- [Supported File Formats](#supported-file-formats)
  - [Input Files](#input-files)
- [Configuration](#configuration)
  - [Display Settings](#display-settings)
  - [Performance Options](#performance-options)
- [Troubleshooting](#troubleshooting)
  - [Common Issues](#common-issues)
  - [Development Guidelines](#development-guidelines) 

## Features

### Main Features
- **Mesh Visualization**: Load and display 2D/3D finite element meshes from .NEU files
- **Field Variables**: Visualize stress, strain, velocity, force and temperature fields...
- **Animation Controls**: Animate deformed mesh sequences with frame-by-frame control
- **Interactive Analysis**: Click-based inspection of elements and nodes with detailed information
- **Multiple Display Modes**: Contour, vector field and high-definition visualization
- **Constraint Visualization**: Display boundary conditions and contact nodes
- **Automatic Scaling**: Automatic scale adjustment across multiple mesh files

### Analysis Tools
- **XY Graphics**: Plot force, displacement and other variables over time
- **3D Model Generation**: Convert 2D models to 3D (plane strain, plane stress, axisymmetric)

## Technical Features
- **File Preloading**: Background loading and caching of files for improved real-time performance
- **PyVista Visualization**: Use of PyVista and camera recalibration with left-click to explore meshes

## Prerequisites

### System Configuration
- Python 3.7+
- Windows/Linux/macOS

### Dependencies
```
PyQt5>=5.15.0
pyvista>=0.40.0
pyvistaqt>=0.11.0
numpy>=1.20.0
matplotlib>=3.5.0
vtk>=9.0.0
```

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/maud-genetet/i-form-internship-2025.git
cd i-form-internship-2025
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Launch the application**
```bash
python main.py
```

## Project Structure

```
i-form/
├── main.py                    # Application entry point
├── main_ui.py                 # Auto-generated PyQt5 interface
├── main.ui                    # Qt Designer UI file
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── .gitignore                 # Git exclusion rules
│
├── handlers/                  # Menu and action handlers
│   ├── __init__.py
│   ├── graphics/              # Graphics-specific components
│   │   ├── __init__.py
│   │   └── xy_graphics_dialog.py  # XY plotting dialog + graphics creation
│   ├── animation_handler.py   # Animation controls
│   ├── build_3d_handler.py    # 3D model generation + dialogs
│   ├── field_variables_handler.py # Variable management
│   ├── file_handler.py        # File tab
│   ├── graphics_handler.py    # Graphics tab
│   └── mesh_handler.py        # Mesh management
│
├── parser/                    # File parsing system
│   ├── __init__.py
│   ├── parser_neutral_file.py # .NEU file parser
│   └── models/                # Data models
│       ├── __init__.py
│       ├── die.py             # Die data model
│       ├── element.py         # Element data model
│       ├── neutral_file.py    # Main data container
│       └── node.py            # Node data model
│
├── preloader/                 # Background file loading
│   ├── __init__.py
│   ├── file_preloader.py      # Threaded file loader
│   └── preloader_manager.py   # Loading coordination
│
└── visualization/             # Main visualization system
    ├── __init__.py
    ├── display_modes.py       # Display mode management
    ├── interaction_handler.py # User interaction handling
    ├── mesh_builder.py        # PyVista mesh creation
    ├── toolbar_manager.py     # Toolbar and interface controls
    └── visualization_manager.py # Main visualization controller
```

## Usage Guide

### Getting Started

1. **Set Working Directory**
   - File → Working Directory...
   - Select the folder containing your .NEU files

2. **Visualize Field Variables**
   - Field Variables → [Select variable type]
   - Choose from stress, strain, velocity, force, temperature, etc.

### Main Features

#### Animation Controls
- Access via Animation → Animation Controls...
- Control frame range, playback speed and looping
- Manual frame-by-frame progression with previous/next buttons

#### 3D Model Generation
- Build 3D → [Select model type]
- Convert 2D models to 3D plane strain, plane stress or axisymmetric
- Automatic thickness detection from fem.dat files

#### Interactive Analysis
- Click the "Mesh Info" button in the toolbar
- Select Elements or Nodes mode
- Click on the mesh to inspect detailed information

#### Graphics and Plotting
- Graphics → XY Graphics
- Plot die forces, displacements and velocities over time
- Support for multi-file time series analysis

#### Camera Recalibration
- Use left-click to recalibrate the camera on the current mesh
- Enables interactive mesh exploration
- To reset the view, click the "Reset View" button in the toolbar
- For a flat view, click the "Front View" button in the toolbar
- To zoom the view, use the mouse wheel or your trackpad zoom

### Visualization Options

- **Show Mesh Edges**: Control edge visibility
- **View Constraints**: Display boundary conditions
- **HD Contour**: High-definition smooth contours
- **Vector Mode**: Display vector fields with arrows
- **Auto Scale**: Automatic scaling across mesh sequence from first to last file

## Supported File Formats

### Input Files
- **.NEU files**: Main mesh and results format
- **fem.dat**: Configuration file (thickness)

## Configuration

### Display Settings
- Material colors: Automatic color assignment by material number
- Constraint visualization: Color-coded boundary conditions, adjustable size
- Vector scaling: Adjustable arrow sizes

### Performance Options
- Background preloading: Automatic loading of mesh sequences
- Level of detail: Adaptive quality based on mesh complexity
- Caching: Smart caching of scales and calculated data

## Troubleshooting

### Common Issues

1. **Files not loading**
   - Ensure .NEU files are in correct format
   - Check file permissions and paths
   - Verify working directory is set correctly

2. **Slow performance**
   - Large meshes may require time to load
   - Check available RAM memory
   - If there are too many files, or they are too large, consider changing file preloading with an LRU (Least Recently Used) loading system to avoid loading all files simultaneously

3. **Animation not working**
   - Requires multiple .NEU files (FEM1.NEU, FEM2.NEU, etc.)
   - Files must be in sequential order
   - Ensure all files are valid and complete

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings to all functions and classes
- Include error handling for file operations
- Test with various mesh sizes and formats