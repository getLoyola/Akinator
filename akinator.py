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
        'no_branch': serialize_tree(node.no_branch)
    }

def deserialize_tree(data):
    if data is None:
        return None
    node = TreeNode(data['question'])
    node.yes_branch = deserialize_tree(data['yes_branch'])
    node.no_branch = deserialize_tree(data['no_branch'])
    return node

def ask_question(question):
    return input(f"{question} (yes/no): ").strip().lower()

def traverse_tree(node):
    while not node.is_leaf():
        answer = ask_question(node.question)
        if answer == 'yes':
            node = node.yes_branch
        elif answer == 'no':
            node = node.no_branch
        else:
            print("Please answer with 'yes' or 'no'.")
    return node

def add_new_character(node):
    character = input("I give up! Who was your character? ").strip()
    new_question = input(f"Please provide a question to distinguish {character} from {node.question}: ").strip()
    correct_answer = input(f"For {character}, what would the answer be? (yes/no): ").strip().lower()

    if correct_answer == 'yes':
        new_yes_branch = TreeNode(character)
        new_no_branch = TreeNode(node.question)
    else:
        new_yes_branch = TreeNode(node.question)
        new_no_branch = TreeNode(character)
    
    node.question = new_question
    node.yes_branch = new_yes_branch
    node.no_branch = new_no_branch

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
