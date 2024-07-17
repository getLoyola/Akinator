import json
import tkinter as tk
from tkinter import simpledialog, messagebox
from decision_tree import TreeNode

def load_knowledge_base(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return deserialize_tree(data)
    except FileNotFoundError:
        return TreeNode("Is your character real?")  # Initial question

def save_knowledge_base(file_path, root):
    with open(file_path, 'w') as file:
        json.dump(serialize_tree(root), file, indent=4)

def serialize_tree(node):
    if node is None:
        return None
    return {
        'question': node.question,
        'yes_branch': serialize_tree(node.yes_branch),
        'no_branch': serialize_tree(node.no_branch),
        'yes_count': node.yes_count,
        'no_count': node.no_count
    }

def deserialize_tree(data):
    if data is None:
        return None
    node = TreeNode(data['question'])
    node.yes_branch = deserialize_tree(data['yes_branch'])
    node.no_branch = deserialize_tree(data['no_branch'])
    node.yes_count = data.get('yes_count', 0)
    node.no_count = data.get('no_count', 0)
    return node

class AkinatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Akinator")
        self.knowledge_base = load_knowledge_base('knowledge_base.json')

        self.label = tk.Label(root, text="Think of a character, and I will try to guess it.")
        self.label.pack(pady=20)

        self.question_label = tk.Label(root, text="", font=("Helvetica", 14))
        self.question_label.pack(pady=20)

        self.yes_button = tk.Button(root, text="Yes", command=self.yes)
        self.yes_button.pack(side=tk.LEFT, padx=10, pady=20)

        self.no_button = tk.Button(root, text="No", command=self.no)
        self.no_button.pack(side=tk.RIGHT, padx=10, pady=20)

        self.restart_button = tk.Button(root, text="Restart", command=self.restart)
        self.restart_button.pack(pady=20)

        self.current_node = None
        self.restart()

    def ask_question(self, question):
        self.question_label.config(text=question)

    def traverse_tree(self):
        while not self.current_node.is_leaf():
            return
        self.final_question()

    def yes(self):
        self.current_node.update_counts('yes')
        if self.current_node.yes_branch:
            self.current_node = self.current_node.yes_branch
            self.ask_question(self.current_node.question)
        else:
            self.add_new_character()
        
    def no(self):
        self.current_node.update_counts('no')
        if self.current_node.no_branch:
            self.current_node = self.current_node.no_branch
            self.ask_question(self.current_node.question)
        else:
            self.add_new_character()

    def final_question(self):
        answer = messagebox.askyesno("Final Question", f"Is your character {self.current_node.question}?")
        if answer:
            messagebox.showinfo("Result", "I guessed it!")
            self.restart()
        else:
            self.add_new_character()

    def add_new_character(self):
        character = simpledialog.askstring("New Character", "I give up! Who was your character?")
        if character:
            self.current_node.learn_from_feedback(character)
        self.restart()

    def restart(self):
        self.current_node = self.knowledge_base
        self.ask_question(self.current_node.question)

    def on_closing(self):
        self.knowledge_base.balance_tree()
        save_knowledge_base('knowledge_base.json', self.knowledge_base)
        self.root.destroy()

def main():
    root = tk.Tk()
    app = AkinatorApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
