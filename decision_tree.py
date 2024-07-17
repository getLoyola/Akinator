class TreeNode:
    def __init__(self, question, yes_branch=None, no_branch=None):
        self.question = question
        self.yes_branch = yes_branch
        self.no_branch = no_branch
        self.yes_count = 0
        self.no_count = 0

    def is_leaf(self):
        return self.yes_branch is None and self.no_branch is None

    def update_counts(self, answer):
        if answer == 'yes':
            self.yes_count += 1
        elif answer == 'no':
            self.no_count += 1

    def get_score(self):
        total = self.yes_count + self.no_count
        if total == 0:
            return 0
        return min(self.yes_count, self.no_count) / total

    def learn_from_feedback(self, correct_character):
        new_question = input(f"I couldn't guess it. Please provide a question to distinguish {correct_character} from {self.question}: ").strip()
        correct_answer = input(f"For {correct_character}, what would the answer be? (yes/no): ").strip().lower()

        if correct_answer == 'yes':
            self.yes_branch = TreeNode(correct_character)
            self.no_branch = TreeNode(self.question)
        else:
            self.yes_branch = TreeNode(self.question)
            self.no_branch = TreeNode(correct_character)
        
        self.question = new_question

**Step 2: Implement Feedback in Main Program**

Update `akinator.py` to include feedback and learning functionality.

Update `akinator.py`:

```python
import json
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

def ask_question(question):
    return input(f"{question} (yes/no): ").strip().lower()

def traverse_tree(node):
    while not node.is_leaf():
        answer = ask_question(node.question)
        node.update_counts(answer)
        if answer == 'yes':
            node = node.yes_branch
        elif answer == 'no':
            node = node.no_branch
        else:
            print("Please answer with 'yes' or 'no'.")
    return node

def add_new_character(node):
    character = input("I give up! Who was your character? ").strip()
    node.learn_from_feedback(character)

def main():
    knowledge_base = load_knowledge_base('knowledge_base.json')

    print("Welcome to Akinator!")
    print("Think of a character, and I will try to guess it.")

    while True:
        current_node = traverse_tree(knowledge_base)
        final_answer = ask_question(f"Is your character {current_node.question}?")
        
        if final_answer == 'yes':
            print("I guessed it!")
        else:
            print("I couldn't guess it.")
            add_new_character(current_node)

        if input("Do you want to play again? (yes/no): ").strip().lower() != 'yes':
            break

    save_knowledge_base('knowledge_base.json', knowledge_base)
    print("Thanks for playing!")

if __name__ == "__main__":
    main()
