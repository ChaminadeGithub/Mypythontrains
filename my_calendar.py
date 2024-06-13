import tkinter as tk
import calendar
from tkinter import messagebox
from fpdf import FPDF
import os


class CustomPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, f"Calendrier {year}", 0, 1, "C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")


def show_calendar():
    year = year_entry.get()
    if not year:
        messagebox.showerror("Erreur", "Veuillez entrer une année.")
        return

    try:
        year = int(year)
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer une année valide.")
        return

    cal = calendar.TextCalendar()
    months = [cal.formatmonth(year, month, 2, 1).splitlines() for month in range(1, 13)]

    text_widget.config(state=tk.NORMAL)  # Permettre les modifications temporaires
    text_widget.delete(1.0, tk.END)  # Efface le contenu existant

    num_months = len(months)
    rows_per_column = 4
    cols = 3

    for row in range(rows_per_column):
        for line_index in range(len(months[0])):
            for col in range(cols):
                month_index = col * rows_per_column + row
                if month_index < num_months and line_index < len(months[month_index]):
                    text_widget.insert(tk.END, months[month_index][line_index].center(22))
                text_widget.insert(tk.END, "   ")  # Ajoute un espace entre les colonnes
            text_widget.insert(tk.END, "\n")
        text_widget.insert(tk.END, "\n\n")

    text_widget.config(state=tk.DISABLED)  # Désactiver l'édition


def generate_pdf():
    global year  # Déclarer 'year' comme global pour l'utiliser dans CustomPDF
    year = year_entry.get()
    if not year:
        messagebox.showerror("Erreur", "Veuillez entrer une année.")
        return

    try:
        year = int(year)
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer une année valide.")
        return

    cal = calendar.TextCalendar()
    pdf = CustomPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    months = [cal.formatmonth(year, month, 2, 1).splitlines() for month in range(1, 13)]
    col_width = 190 / 3  # Diviser la largeur de la page par 3 colonnes
    row_height = 277 / 4  # Diviser la hauteur de la page par 4 lignes

    for row in range(4):
        for col in range(3):
            month_index = row * 3 + col
            if month_index < 12:
                x = 10 + col * col_width
                y = 20 + row * row_height
                pdf.set_xy(x, y)
                pdf.multi_cell(col_width, 10, "\n".join(months[month_index]), 0, 'C')

    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    pdf_file = os.path.join(downloads_path, f"calendrier_{year}.pdf")
    pdf.output(pdf_file)

    abs_path = os.path.abspath(pdf_file)
    messagebox.showinfo("Succès", f"Le calendrier {year} a été généré sous {pdf_file}.\nChemin complet: {abs_path}")


# Création de la fenêtre principale
root = tk.Tk()
root.title("Calendrier")
root.geometry("800x600")
root.configure(bg='yellow')

# Empêcher le redimensionnement de la fenêtre
root.resizable(False, False)

# Ajout d'une étiquette et d'un champ de saisie pour l'année
year_label = tk.Label(root, text="Entrer l'année :", bg='yellow')
year_label.pack(pady=10)
year_entry = tk.Entry(root)
year_entry.pack(pady=10)

# Ajout d'un bouton pour générer le calendrier
generate_button = tk.Button(root, text="Générer le calendrier", command=show_calendar)
generate_button.pack(pady=10)

# Ajout d'un bouton pour générer le PDF
pdf_button = tk.Button(root, text="Imprimer en PDF", command=generate_pdf)
pdf_button.pack(pady=10)

# Ajout d'un widget de texte pour afficher le calendrier
text_widget = tk.Text(root, wrap='none')
text_widget.pack(expand=1, fill='both')
text_widget.config(state=tk.DISABLED)  # Désactiver l'édition initialement

# Définir les styles pour les tags (vous pouvez ajouter plus de styles si nécessaire)
text_widget.tag_configure("month1", foreground="red")
text_widget.tag_configure("month2", foreground="blue")
text_widget.tag_configure("month3", foreground="green")
text_widget.tag_configure("month4", foreground="purple")
text_widget.tag_configure("month5", foreground="orange")
text_widget.tag_configure("month6", foreground="cyan")
text_widget.tag_configure("month7", foreground="magenta")
text_widget.tag_configure("month8", foreground="yellow", background="black")
text_widget.tag_configure("month9", foreground="pink")
text_widget.tag_configure("month10", foreground="brown")
text_widget.tag_configure("month11", foreground="lime")
text_widget.tag_configure("month12", foreground="violet")

# Démarrage de la boucle principale de l'application
root.mainloop()
