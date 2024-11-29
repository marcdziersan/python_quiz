import tkinter as tk
from tkinter import messagebox, simpledialog
import json

# Lade oder erstelle die Quiz-Daten
def lade_quiz_daten(datei):
    try:
        with open(datei, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def speichere_quiz_daten(datei, daten):
    with open(datei, 'w', encoding='utf-8') as f:
        json.dump(daten, f, indent=4, ensure_ascii=False)

quiz_data = lade_quiz_daten("quiz_data.json")

class QuizVerwaltungApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz-Verwaltung")
        self.root.geometry("900x600")
        self.quiz_data = quiz_data

        # Hauptmenü
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        # Datei Menü
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Save", command=self.speichern)

        # Quiz Menü
        self.quiz_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Quiz", menu=self.quiz_menu)
        self.quiz_menu.add_command(label="Add", command=self.create_question)

        # Hauptbereich für die Anzeige der Fragenliste
        self.main_frame = tk.Frame(self.root, bg='#ecf0f1', padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas und Scrollbar für die Frage-Liste
        self.canvas = tk.Canvas(self.main_frame, bg='#ecf0f1')
        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.list_frame = tk.Frame(self.canvas, bg='#ecf0f1')
        self.canvas.create_window((0, 0), window=self.list_frame, anchor="nw")
        self.list_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Aktualisiere die Anzeige
        self.update_question_list()

    def speichern(self):
        speichere_quiz_daten("quiz_data.json", self.quiz_data)
        messagebox.showinfo("Info", "Daten erfolgreich gespeichert.")
        self.update_question_list()

    def create_question(self):
        frage = simpledialog.askstring("Neue Frage", "Geben Sie die Frage ein:")
        if not frage:
            return

        optionen = []
        for i in range(4):
            option = simpledialog.askstring(f"Option {i+1}", f"Geben Sie die Antwortmöglichkeit {i+1} ein:")
            if option:
                optionen.append(option)

        antwort = simpledialog.askstring("Richtige Antwort", "Geben Sie die richtige Antwort ein:")
        if antwort not in optionen:
            messagebox.showwarning("Warnung", "Die richtige Antwort muss eine der Antwortmöglichkeiten sein.")
            return

        neue_frage = {
            "frage": frage,
            "optionen": optionen,
            "antwort": antwort
        }

        self.quiz_data.append(neue_frage)
        messagebox.showinfo("Info", "Frage erfolgreich hinzugefügt.")
        self.speichern()

    def update_question_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        for i, frage_data in enumerate(self.quiz_data):
            frage_label = tk.Label(self.list_frame, text=f"Frage {i+1}: {frage_data['frage']}", font=('Arial', 10), bg='#ecf0f1', anchor="w", wraplength=700, justify="left")
            frage_label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            edit_button = tk.Button(self.list_frame, text="Edit", command=lambda i=i: self.edit_question(i), font=('Arial', 10), bg='#3498db', fg='#ecf0f1', cursor='hand2', bd=0)
            edit_button.grid(row=i, column=1, padx=10, pady=5)

            delete_button = tk.Button(self.list_frame, text="Delete", command=lambda i=i: self.delete_question(i), font=('Arial', 10), bg='#e74c3c', fg='#ecf0f1', cursor='hand2', bd=0)
            delete_button.grid(row=i, column=2, padx=10, pady=5)

    def edit_question(self, index):
        frage_data = self.quiz_data[index]

        popup = tk.Toplevel(self.root)
        popup.title("Frage bearbeiten")
        popup.geometry("400x400")
        popup.config(bg='#ecf0f1')

        frage_label = tk.Label(popup, text="Frage:", font=('Arial', 10), bg='#ecf0f1')
        frage_label.pack(pady=10)
        frage_entry = tk.Entry(popup, font=('Arial', 10), width=50)
        frage_entry.insert(0, frage_data["frage"])
        frage_entry.pack(pady=10)

        option_entries = []
        for i in range(4):
            option_label = tk.Label(popup, text=f"Antwort {i+1}:", font=('Arial', 10), bg='#ecf0f1')
            option_label.pack(pady=5)
            option_entry = tk.Entry(popup, font=('Arial', 10), width=50)
            option_entry.insert(0, frage_data["optionen"][i])
            option_entry.pack(pady=5)
            option_entries.append(option_entry)

        def save_changes():
            frage_data["frage"] = frage_entry.get()
            for i, option_entry in enumerate(option_entries):
                frage_data["optionen"][i] = option_entry.get()

            antwort = simpledialog.askstring("Richtige Antwort", "Geben Sie die richtige Antwort ein:", initialvalue=frage_data["antwort"])
            if antwort not in frage_data["optionen"]:
                messagebox.showwarning("Warnung", "Die richtige Antwort muss eine der Antwortmöglichkeiten sein.")
                return

            frage_data["antwort"] = antwort
            self.speichern()
            popup.destroy()

        save_button = tk.Button(popup, text="Speichern", command=save_changes, font=('Arial', 10), bg='#2ecc71', fg='#ecf0f1', cursor='hand2', bd=0)
        save_button.pack(pady=20)

    def delete_question(self, index):
        frage_data = self.quiz_data.pop(index)
        messagebox.showinfo("Info", f"Frage '{frage_data['frage']}' erfolgreich gelöscht.")
        self.speichern()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizVerwaltungApp(root)
    root.mainloop()
