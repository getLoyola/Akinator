import json

def load_knowledge_base(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_knowledge_base(file_path, knowledge_base):
    with open(file_path, 'w') as file:
        json.dump(knowledge_base, file, indent=4)

def ask_question(question):
    return input(f"{question} (yes/no): ").strip().lower()

def main():
    knowledge_base = load_knowledge_base('knowledge_base.json')

    print("Welcome to Akinator!")
    print("Think of a character, and I will try to guess it.")

    while True:
        question = "Is your character real?"
        answer = ask_question(question)

        if answer in ('yes', 'no'):
            print(f"You answered: {answer}")
            # Further logic will be added in future iterations
        else:
            print("Please answer with 'yes' or 'no'.")

        if input("Do you want to play again? (yes/no): ").strip().lower() != 'yes':
            break

    save_knowledge_base('knowledge_base.json', knowledge_base)
    print("Thanks for playing!")

if __name__ == "__main__":
    main()
