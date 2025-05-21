import tkinter as tk
from tkinter import messagebox, font

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Application Accessible")
        self.geometry("400x300")

        # Police dynamique
        self.base_font_size = 10
        self.default_font = font.Font(family="Helvetica", size=self.base_font_size)

        self.creer_barre_personnalisee()
        self.creer_contenu()

    def creer_barre_personnalisee(self):
        self.barre = tk.Frame(self, bg="#f0f0f0")
        self.barre.pack(fill=tk.X)

        bouton_fichier = tk.Menubutton(self.barre, text="Fichier", font=self.default_font)
        menu = tk.Menu(bouton_fichier, tearoff=0, font=self.default_font)
        menu.add_command(label="Ouvrir", command=self.open_dialog_box)
        menu.add_separator()
        menu.add_command(label="Quitter", command=self.quit)
        bouton_fichier.config(menu=menu)
        bouton_fichier.pack(side=tk.LEFT, padx=5, pady=2)

        bouton_plus = tk.Button(self.barre, text="+", font=self.default_font, command=self.zoom_in)
        bouton_plus.pack(side=tk.LEFT, padx=5)

        bouton_moins = tk.Button(self.barre, text="-", font=self.default_font, command=self.zoom_out)
        bouton_moins.pack(side=tk.LEFT, padx=5)

        bouton_apropos = tk.Button(self.barre, text="À propos", font=self.default_font,
                                   command=lambda: messagebox.showinfo("À propos", "Ceci est une application accessible."))
        bouton_apropos.pack(side=tk.LEFT, padx=5)

    def creer_contenu(self):
        self.label = tk.Label(self, text="Contenu principal", font=self.default_font)
        self.label.pack(pady=50)

    def zoom_in(self):
        self.base_font_size += 1
        self.update_fonts()

    def zoom_out(self):
        self.base_font_size = max(6, self.base_font_size - 1)
        self.update_fonts()

    def update_fonts(self):
        self.default_font.configure(size=self.base_font_size)

    def open_dialog_box(self):
        messagebox.showinfo("Fenêtre", "Fenêtre")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
