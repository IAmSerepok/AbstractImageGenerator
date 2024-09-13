import numpy as np
from constants import WIDTH, HEIGHT


SIZE = (WIDTH + HEIGHT) / 2


class Node:
    def __init__(self):
        self.parents = None


# Binary nodes
class MullNode(Node):
    def operate(self, x, y):
        left, right = self.parents
        return left.operate(x, y) * right.operate(x, y)

    def get_func_string(self):
        left, right = self.parents
        return f'{left.get_func_string()} * {right.get_func_string()}'


class DivideNode(Node):
    def operate(self, x, y):
        left, right = self.parents
        left, right = left.operate(x, y), right.operate(x, y)
        if right != 0:
            result = left / right
        else:
            result = left
        return result

    def get_func_string(self):
        left, right = self.parents
        return f'{left.get_func_string()} / {right.get_func_string()}'


class AddNode(Node):
    def operate(self, x, y):
        left, right = self.parents
        return left.operate(x, y) + right.operate(x, y)

    def get_func_string(self):
        left, right = self.parents
        return f'{left.get_func_string()} + {right.get_func_string()}'


class SubtractNode(Node):
    def operate(self, x, y):
        left, right = self.parents
        return left.operate(x, y) - right.operate(x, y)

    def get_func_string(self):
        left, right = self.parents
        return f'{left.get_func_string()} - {right.get_func_string()}'


class Arctan2Node(Node):
    def operate(self, x, y):
        left, right = self.parents
        return np.arctan2(left.operate(x, y), right.operate(x, y))

    def get_func_string(self):
        left, right = self.parents
        return f'arctan2({left.get_func_string()}, {right.get_func_string()})'


binary_nodes = [MullNode, AddNode, SubtractNode, Arctan2Node, DivideNode]


# Unary nodes
class SinNode(Node):
    def operate(self, x, y):
        return np.sin(self.parents[0].operate(x, y))

    def get_func_string(self):
        return f'sin({self.parents[0].get_func_string()})'


class ArctanNode(Node):
    def operate(self, x, y):
        return np.arctan(self.parents[0].operate(x, y))

    def get_func_string(self):
        return f'arctan({self.parents[0].get_func_string()})'


class LogNode(Node):
    def operate(self, x, y):
        result = self.parents[0].operate(x, y)
        if result > 0:
            result = np.log(result)
        return result

    def get_func_string(self):
        return f'ln({self.parents[0].get_func_string()})'


class ArcsinhNode(Node):
    def operate(self, x, y):
        return np.arcsinh(self.parents[0].operate(x, y))

    def get_func_string(self):
        return f'arcsinh({self.parents[0].get_func_string()})'


class SqrtNode(Node):
    def operate(self, x, y):
        result = self.parents[0].operate(x, y)
        if result > 0:
            result = np.sqrt(result)
        return result

    def get_func_string(self):
        return f'sqrt({self.parents[0].get_func_string()})'


unary_nodes = [SinNode, LogNode, ArctanNode, SqrtNode, ArcsinhNode]


# Constant nodes
class ConstantNode(Node):
    def __init__(self):
        super().__init__()
        value = -1 if np.random.random() < 0.5 else 1
        value *= np.random.random() * SIZE
        self.value = value

    def operate(self, x, y):
        return self.value

    def get_func_string(self):
        return f'{self.value}'


class VarXNode(Node):
    def operate(self, x, y):
        return x

    def get_func_string(self):
        return 'x'


class VaYNode(Node):
    def operate(self, x, y):
        return y

    def get_func_string(self):
        return 'y'


constant_nodes = [ConstantNode, VarXNode, VaYNode]

# all nodes
nodes = {0: constant_nodes, 1: unary_nodes, 2: binary_nodes}
