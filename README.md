# i-form-internship-2025

TO DO: Make documentation 

## Installation

Install dependencies
```bash	
pip install -r requirements.txt
```

## Usage
```bash
python main.py
```

## File Structure
```plaintext
i-form-visualization/
├── main.py                          # Main application entry point
├── main_ui.py                       # Generated UI file (PyQt5)
├── modules/
│   ├── __init__.py
│   ├── file_handler.py             # File operations
│   ├── mesh_handler.py             # Mesh loading and management
│   ├── field_variables_handler.py  # Field variables visualization
│   ├── visualization/              # PyVista visualization modules
│   │   ├── __init__.py
│   │   ├── core.py                 # Main visualization manager
│   │   ├── mesh_builder.py         # PyVista mesh creation
│   │   ├── display_modes.py        # Display mode management
│   │   └── interaction_handler.py  # User interaction handling
│   └── parser/                     # Neutral file parsing
│       ├── __init__.py
│       ├── ParserNeutralFile.py    # Main parser
│       ├── NeutralFile.py          # Data container
│       ├── Node.py                 # Node data structure
│       ├── Element.py              # Element data structure
│       └── Die.py                  # Die data structure
```