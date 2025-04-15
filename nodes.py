import numpy as np
from constants import WIDTH, HEIGHT

# Глобальная константа для генерации случайных значений
SIZE = (WIDTH + HEIGHT) / 2

class Node:
    """Базовый класс для всех узлов дерева операций.
    
    Attributes:
        parents (list[Node] | None): Родительские узлы. None для терминальных узлов.
    """
    def __init__(self):
        self.parents = None

    def get_func_string(self) -> str:
        """Возвращает строковое представление операции в узле"""
        ...


# Бинарные узлы (принимают два аргумента)
class MullNode(Node):
    """Узел для операции умножения."""
    def operate(self, x: float, y: float) -> float:
        left, right = self.parents
        return left.operate(x, y) * right.operate(x, y)

    def get_func_string(self) -> str:
        left, right = self.parents
        return f'{left.get_func_string()} * {right.get_func_string()}'


class DivideNode(Node):
    """Узел для операции деления с защитой от деления на ноль."""
    def operate(self, x: float, y: float) -> float:
        left, right = self.parents
        left_val, right_val = left.operate(x, y), right.operate(x, y)
        return left_val if right_val == 0 else left_val / right_val

    def get_func_string(self) -> str:
        left, right = self.parents
        return f'{left.get_func_string()} / {right.get_func_string()}'


class AddNode(Node):
    """Узел для операции сложения."""
    def operate(self, x: float, y: float) -> float:
        left, right = self.parents
        return left.operate(x, y) + right.operate(x, y)

    def get_func_string(self) -> str:
        left, right = self.parents
        return f'{left.get_func_string()} + {right.get_func_string()}'


class SubtractNode(Node):
    """Узел для операции вычитания."""
    def operate(self, x: float, y: float) -> float:
        left, right = self.parents
        return left.operate(x, y) - right.operate(x, y)

    def get_func_string(self) -> str:
        left, right = self.parents
        return f'{left.get_func_string()} - {right.get_func_string()}'


class Arctan2Node(Node):
    """Узел для вычисления арктангенса от отношения (y/x)."""
    def operate(self, x: float, y: float) -> float:
        left, right = self.parents
        return np.arctan2(left.operate(x, y), right.operate(x, y))

    def get_func_string(self) -> str:
        left, right = self.parents
        return f'arctan2({left.get_func_string()}, {right.get_func_string()})'


# Список всех бинарных операций
binary_nodes = [MullNode, AddNode, SubtractNode, Arctan2Node, DivideNode]


# Унарные узлы (принимают один аргумент)
class SinNode(Node):
    """Узел для вычисления синуса."""
    def operate(self, x: float, y: float) -> float:
        return np.sin(self.parents[0].operate(x, y))

    def get_func_string(self) -> str:
        return f'sin({self.parents[0].get_func_string()})'


class ArctanNode(Node):
    """Узел для вычисления арктангенса."""
    def operate(self, x: float, y: float) -> float:
        return np.arctan(self.parents[0].operate(x, y))

    def get_func_string(self) -> str:
        return f'arctan({self.parents[0].get_func_string()})'


class LogNode(Node):
    """Узел для вычисления натурального логарифма."""
    def operate(self, x: float, y: float) -> float:
        result = self.parents[0].operate(x, y)
        return np.log(result) if result > 0 else result

    def get_func_string(self) -> str:
        return f'ln({self.parents[0].get_func_string()})'


class ArcsinhNode(Node):
    """Узел для вычисления гиперболического арксинуса."""
    def operate(self, x: float, y: float) -> float:
        return np.arcsinh(self.parents[0].operate(x, y))

    def get_func_string(self) -> str:
        return f'arcsinh({self.parents[0].get_func_string()})'


class SqrtNode(Node):
    """Узел для вычисления квадратного корня."""
    def operate(self, x: float, y: float) -> float:
        result = self.parents[0].operate(x, y)
        return np.sqrt(result) if result > 0 else result

    def get_func_string(self) -> str:
        return f'sqrt({self.parents[0].get_func_string()})'


# Список всех унарных операций
unary_nodes = [SinNode, LogNode, ArctanNode, SqrtNode, ArcsinhNode]


# Терминальные узлы (листья дерева)
class ConstantNode(Node):
    """Узел-константа со случайным значением."""
    def __init__(self):
        super().__init__()
        # Генерация случайного значения в диапазоне [-SIZE, SIZE]
        self.value = (-1 if np.random.random() < 0.5 else 1) * np.random.random() * SIZE

    def operate(self, x: float, y: float) -> float:
        return self.value

    def get_func_string(self) -> str:
        return f'{self.value}'


class VarXNode(Node):
    """Узел для переменной X."""
    def operate(self, x: float, y: float) -> float:
        return x

    def get_func_string(self) -> str:
        return 'x'


class VarYNode(Node):
    """Узел для переменной Y."""
    def operate(self, x: float, y: float) -> float:
        return y

    def get_func_string(self) -> str:
        return 'y'


# Список всех терминальных узлов
constant_nodes = [ConstantNode, VarXNode, VarYNode]

# Иерархия всех узлов по количеству аргументов
nodes = {
    0: constant_nodes,  # Терминалы
    1: unary_nodes,     # Унарные операции
    2: binary_nodes     # Бинарные операции
}
