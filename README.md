# i-form-internship-2025

TO DO: Make documentation 

## Install dependencies

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
├── main.ui                          # Main UI file ( We don't need to keep it, it is just for generating main_ui.py )
├── main.py                          # Main application entry point
├── main_ui.py                       # Generated UI file (PyQt5) !!! Do not edit directly !!!
├── modules/
|   |
│   ├── __init__.py
│   ├── file_handler.py             # File tab
│   ├── mesh_handler.py             # Mesh tab ( to delete ? )
│   ├── field_variables_handler.py  # Field variables tab ( to delete ?)
|   |
│   ├── visualization/              # PyVista visualization modules
│   │   ├── __init__.py
│   │   ├── core.py                 # Main visualization manager
│   │   ├── mesh_builder.py         # PyVista mesh creation
│   │   ├── display_modes.py        # Display mode management
│   │   └── interaction_handler.py  # Click tracking
|   |                               
│   └── parser/                     # Parser for NEU files : this module is complete, if we change the format, we need to 
        |                           # change the parser
│       ├── __init__.py
│       ├── ParserNeutralFile.py    # Main parser
│       ├── NeutralFile.py          # Data container
│       ├── Node.py                 # Node data structure
│       ├── Element.py              # Element data structure
│       └── Die.py                  # Die data structure
```