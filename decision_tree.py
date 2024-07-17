class TreeNode:
    def __init__(self, question, yes_branch=None, no_branch=None):
        self.question = question
        self.yes_branch = yes_branch
        self.no_branch = no_branch

    def is_leaf(self):
        return self.yes_branch is None and self.no_branch is None
