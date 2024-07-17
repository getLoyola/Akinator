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

    def traverse(self):
        answer = input(f"{self.question} (yes/no): ").strip().lower()
        while answer not in ['yes', 'no']:
            print("Please answer with 'yes' or 'no'.")
            answer = input(f"{self.question} (yes/no): ").strip().lower()

        if answer == 'yes':
            if self.yes_branch:
                self.yes_branch.traverse()
            else:
                self.learn_from_feedback("character")
        elif answer == 'no':
            if self.no_branch:
                self.no_branch.traverse()

    def balance_tree(self):
        nodes = self.collect_nodes()
        nodes.sort(key=lambda x: max(x[1], x[2]))  # Sort nodes by the maximum count
        balanced_root = self.build_balanced_tree(nodes)
        self.update_from_balanced_tree(balanced_root)

    def collect_nodes(self):
        if self.is_leaf():
            return [(self.question, self.yes_count, self.no_count)]
        nodes = []
        if self.yes_branch:
            nodes.extend(self.yes_branch.collect_nodes())
        if self.no_branch:
            nodes.extend(self.no_branch.collect_nodes())
        nodes.append((self.question, self.yes_count, self.no_count))
        return nodes

    def build_balanced_tree(self, nodes):
        if not nodes:
            return None
        if len(nodes) == 1:
            return TreeNode(nodes[0][0])
        mid = len(nodes) // 2
        root = TreeNode(nodes[mid][0])
        root.yes_branch = self.build_balanced_tree(nodes[:mid])
        root.no_branch = self.build_balanced_tree(nodes[mid + 1:])
        return root

    def update_from_balanced_tree(self, balanced_root):
        self.question = balanced_root.question
        self.yes_branch = balanced_root.yes_branch
        self.no_branch = balanced_root.no_branch
