import tkinter as tk
from tkinter import simpledialog, messagebox
import akinator

class AkinatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Akinator")
        self.root.geometry("500x400")
        self.root.configure(bg="#f0f0f0")

        self.frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        self.title_label = tk.Label(self.frame, text="Akinator", font=("Helvetica", 24, "bold"), bg="#ffffff")
        self.title_label.pack(pady=10)

        self.instruction_label = tk.Label(self.frame, text="Think of a character, and I will try to guess it.", font=("Helvetica", 14), bg="#ffffff")
        self.instruction_label.pack(pady=10)

        self.question_label = tk.Label(self.frame, text="", font=("Helvetica", 14), bg="#ffffff", wraplength=400)
        self.question_label.pack(pady=20)

        self.button_frame = tk.Frame(self.frame, bg="#ffffff")
        self.button_frame.pack(pady=10)

        self.yes_button = tk.Button(self.button_frame, text="Yes", command=lambda: self.answer('y'), font=("Helvetica", 12), bg="#4CAF50", fg="#ffffff", activebackground="#45a049", padx=20, pady=10)
        self.yes_button.grid(row=0, column=0, padx=10)

        self.no_button = tk.Button(self.button_frame, text="No", command=lambda: self.answer('n'), font=("Helvetica", 12), bg="#f44336", fg="#ffffff", activebackground="#e41f1f", padx=20, pady=10)
        self.no_button.grid(row=0, column=1, padx=10)

        self.dont_know_button = tk.Button(self.button_frame, text="Don't Know", command=lambda: self.answer('idk'), font=("Helvetica", 12), bg="#ff9800", fg="#ffffff", activebackground="#ff7800", padx=20, pady=10)
        self.dont_know_button.grid(row=1, column=0, padx=10, pady=10)

        self.probably_button = tk.Button(self.button_frame, text="Probably", command=lambda: self.answer('p'), font=("Helvetica", 12), bg="#00bcd4", fg="#ffffff", activebackground="#00a4c4", padx=20, pady=10)
        self.probably_button.grid(row=1, column=1, padx=10, pady=10)

        self.probably_not_button = tk.Button(self.button_frame, text="Probably Not", command=lambda: self.answer('pn'), font=("Helvetica", 12), bg="#9c27b0", fg="#ffffff", activebackground="#8c24a0", padx=20, pady=10)
        self.probably_not_button.grid(row=1, column=2, padx=10, pady=10)

        self.restart_button = tk.Button(self.frame, text="Restart", command=self.restart, font=("Helvetica", 12), bg="#008CBA", fg="#ffffff", activebackground="#007bb5", padx=20, pady=10)
        self.restart_button.pack(pady=20)

        self.save_button = tk.Button(self.frame, text="Save Progress", command=self.save_progress, font=("Helvetica", 12), bg="#4CAF50", fg="#ffffff", activebackground="#45a049", padx=20, pady=10)
        self.save_button.pack(pady=10)

        self.load_button = tk.Button(self.frame, text="Load Progress", command=self.load_progress, font=("Helvetica", 12), bg="#f44336", fg="#ffffff", activebackground="#e41f1f", padx=20, pady=10)
        self.load_button.pack(pady=10)

        self.sessions = []

        self.aki = akinator.Akinator()
        self.restart()

    def ask_question(self, question):
        self.question_label.config(text=question)

    def answer(self, ans):
        try:
            self.aki.answer(ans)
            self.ask_question(self.aki.question)
        except akinator.AkiNoQuestions:
            self.make_guess()

    def make_guess(self):
        guess = self.aki.win()
        answer = messagebox.askyesno("Final Guess", f"Is your character {guess['name']}?\n\n{guess['description']}")
        if answer:
            messagebox.showinfo("Result", "I guessed it!")
        else:
            messagebox.showinfo("Result", "You win! I couldn't guess it.")
        self.restart()

    def restart(self):
        self.aki.start_game()
        self.ask_question(self.aki.question)

    def save_progress(self):
        session_name = simpledialog.askstring("Save Progress", "Enter a name for your session:")
        if session_name:
            session_data = {
                'session_name': session_name,
                'progress': self.aki.progression,
                'question': self.aki.question,
                'step': self.aki.step,
                'answer': self.aki.answer,
                'guesses': self.aki.guesses,
            }
            self.sessions.append(session_data)
            messagebox.showinfo("Save Progress", f"Progress saved as '{session_name}'.")

    def load_progress(self):
        session_names = [session['session_name'] for session in self.sessions]
        session_name = simpledialog.askstring("Load Progress", "Choose a session to load:", initialvalue=session_names[0] if session_names else '')
        if session_name:
            for session in self.sessions:
                if session['session_name'] == session_name:
                    self.aki.progression = session['progress']
                    self.aki.question = session['question']
                    self.aki.step = session['step']
                    self.aki.answer = session['answer']
                    self.aki.guesses = session['guesses']
                    self.ask_question(self.aki.question)
                    messagebox.showinfo("Load Progress", f"Progress loaded from '{session_name}'.")
                    return
            messagebox.showwarning("Load Progress", f"No session found with the name '{session_name}'.")

def main():
    root = tk.Tk()
    app = AkinatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
