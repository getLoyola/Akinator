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
