import numpy as np
from nodes import nodes
from constants import MAX_DEPTH


class Tree:
    def __init__(self):
        self.max_depth = MAX_DEPTH
        self.root = None

    def random(self):
        len1, len2 = len(nodes[1]), len(nodes[2])

        if np.random.randint(0, len1 + len2) < len1:
            root = np.random.choice(nodes[1])()
            root.parents = self.generate_parents(1, 1)
        else:
            root = np.random.choice(nodes[2])()
            root.parents = self.generate_parents(1, 2)

        self.root = root
        return self

    def generate_parents(self, depth, length):
        parents = []
        len1, len2 = len(nodes[1]), len(nodes[2])

        for _1 in range(length):
            probability = ((depth - 1) / (self.max_depth - 1)) ** 2
            if np.random.random() < probability:
                parents.append(np.random.choice(nodes[0])())

            elif np.random.randint(0, len1 + len2) < len1:
                parent = np.random.choice(nodes[1])()
                parent.parents = self.generate_parents(depth + 1, 1)
                parents.append(parent)

            else:
                parent = np.random.choice(nodes[2])()
                parent.parents = self.generate_parents(depth + 1, 2)
                parents.append(parent)

        return parents

    def operate(self, x, y):
        return self.root.operate(x, y)

    def get_function_string(self):
        return self.root.get_func_string()
