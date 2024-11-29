import tkinter as tk
import json
import random

# Lade Quiz-Daten aus JSON-Datei mit UTF-8 Kodierung
def lade_quiz_daten(datei):
    with open(datei, 'r', encoding='utf-8') as f:
        return json.load(f)

quiz_data = lade_quiz_daten("quiz_data.json")

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fachinformatiker Quiz")
        self.root.geometry("800x600")  # Feste Fenstergröße

        # Hintergrundfarbe
        self.root.configure(bg='#2c3e50')

        # Rahmen für den gesamten Inhalt
        self.frame = tk.Frame(root, bg='#34495e', padx=20, pady=20)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Frage-Label
        self.frage_label = tk.Label(self.frame, text="", font=('Helvetica', 16, 'bold'), fg='#ecf0f1', bg='#34495e', wraplength=560)
        self.frage_label.pack(pady=20)

        # Variable für die Optionen
        self.options = tk.StringVar(value="")
        self.option_buttons = []

        # Erstelle Radiobuttons für die Antwortmöglichkeiten
        for i in range(4):
            btn = tk.Radiobutton(self.frame, text="", variable=self.options, value="", font=('Helvetica', 14), fg='#ecf0f1', bg='#34495e', activebackground='#16a085', activeforeground='#ecf0f1', selectcolor='#2c3e50', wraplength=500, justify="left")
            btn.pack(anchor="w", padx=20, pady=5)
            self.option_buttons.append(btn)

        # Überprüfen-Schaltfläche
        self.check_button = tk.Button(self.frame, text="Überprüfen", command=self.check_answer, font=('Helvetica', 14, 'bold'), bg='#16a085', fg='#ecf0f1', activebackground='#1abc9c', activeforeground='#ecf0f1', cursor='hand2', bd=0)
        self.check_button.pack(pady=20)

        # Feedback-Label
        self.feedback_label = tk.Label(self.frame, text="", font=('Helvetica', 14), fg='#e74c3c', bg='#34495e')
        self.feedback_label.pack(pady=20)

        # Fragen vorbereiten
        self.questions = self.shuffle_questions(quiz_data, limit=10)
        self.correct_answers = 0
        self.total_questions = len(self.questions)
        self.current_question = 0
        self.show_question()

    def shuffle_questions(self, questions, limit=None):
        # Fragen mischen
        shuffled = questions[:]
        random.shuffle(shuffled)
        if limit:
            shuffled = shuffled[:limit]
        return shuffled

    def shuffle_options(self, question_data):
        # Optionen mischen und den Index der richtigen Antwort zurückgeben
        options = question_data["optionen"][:]
        random.shuffle(options)
        correct_index = options.index(question_data["antwort"])
        return options, correct_index

    def show_question(self):
        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            self.frage_label.config(text=question_data["frage"])

            options, correct_index = self.shuffle_options(question_data)
            
            for i, option in enumerate(options):
                self.option_buttons[i].config(text=option, value=option)

            self.feedback_label.config(text="")
            self.options.set("")
        else:
            self.show_evaluation()

    def check_answer(self):
        selected_option = self.options.get()
        if not selected_option:
            self.feedback_label.config(text="Bitte wähle eine Antwort aus.", fg="#e74c3c")
            return

        correct_answer = self.questions[self.current_question]["antwort"]

        if selected_option == correct_answer:
            self.feedback_label.config(text="Richtig!", fg="#2ecc71")
            self.correct_answers += 1
        else:
            self.feedback_label.config(text=f"Falsch! Die richtige Antwort war: {correct_answer}", fg="#e74c3c")

        self.current_question += 1
        self.root.after(2000, self.show_question)  # Nächste Frage nach 2 Sekunden

    def show_evaluation(self):
        # Entferne alte Widgets
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Zeige die Auswertung an
        auswertung_text = f"Quiz abgeschlossen!\n\nRichtige Antworten: {self.correct_answers} von {self.total_questions}"
        if self.correct_answers == self.total_questions:
            auswertung_text += "\n\nPerfekt! Alle Fragen richtig beantwortet!"
        elif self.correct_answers >= self.total_questions // 2:
            auswertung_text += "\n\nGut gemacht!"
        else:
            auswertung_text += "\n\nMehr Übung erforderlich. Versuche es erneut!"

        auswertung_label = tk.Label(self.frame, text=auswertung_text, font=('Helvetica', 16, 'bold'), fg='#ecf0f1', bg='#34495e', wraplength=560, justify="center")
        auswertung_label.pack(pady=20)

        # Schließen-Button
        close_button = tk.Button(self.frame, text="Schließen", command=self.root.destroy, font=('Helvetica', 14, 'bold'), bg='#e74c3c', fg='#ecf0f1', activebackground='#c0392b', activeforeground='#ecf0f1', cursor='hand2', bd=0)
        close_button.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
