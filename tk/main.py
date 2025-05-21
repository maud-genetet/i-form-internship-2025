import tkinter as tk
from tkinter import messagebox

def open_dialog_box():
    messagebox.showinfo("Windows", "Windows")

# Create a main window
window = tk.Tk()
window.title("Application")
window.geometry("400x300")

# Create a menu bar
menu_bar = tk.Menu(window)

# Create a menu item
menu_item = tk.Menu(menu_bar, tearoff=0)
menu_item.add_command(label="Open", command=open_dialog_box)
menu_bar.add_cascade(label="File", menu=menu_item)
menu_bar.add_command(label="Exit", command=window.quit)
menu_bar.add_command(label="About", command=lambda: messagebox.showinfo("About", "This is a simple application."))
menu_bar.add_separator()
menu_bar.add_command(label="Quit", command=window.quit)
menu_bar.add_command(label="Label", command=lambda: messagebox.showinfo("Label", "Label"))
menu_bar.add_command(label="Button", command=lambda: messagebox.showinfo("Button", "Button"))

# Attach the menu bar to the window
window.config(menu=menu_bar)

# Launch the application
window.mainloop()
