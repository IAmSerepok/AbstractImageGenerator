import numpy as np
from nodes import nodes
from constants import MAX_DEPTH


class Tree:
    """Класс для генерации и работы с синтаксическими деревьями математических выражений.

    Дерево состоит из узлов (Node), которые могут быть:
    - Терминалами (константы, переменные)
    - Унарными операциями (sin, log и т.д.)
    - Бинарными операциями (+, -, *, / и т.д.)

    Attributes:
        max_depth (int): Максимальная глубина дерева (из constants.MAX_DEPTH).
        root (Node): Корневой узел дерева.
    """

    def __init__(self):
        """Инициализирует пустое дерево с максимальной глубиной из constants.MAX_DEPTH."""
        self.max_depth = MAX_DEPTH
        self.root = None

    def random(self) -> 'Tree':
        """Генерирует случайное дерево выражений.

        Returns:
            Tree: Возвращает self для цепочки вызовов.
        """
        len1, len2 = len(nodes[1]), len(nodes[2])

        # Выбираем случайный корневой узел (унарный или бинарный)
        if np.random.randint(0, len1 + len2) < len1:
            root = np.random.choice(nodes[1])()
            root.parents = self.generate_parents(1, 1)
        else:
            root = np.random.choice(nodes[2])()
            root.parents = self.generate_parents(1, 2)

        self.root = root
        return self

    def generate_parents(self, depth: int, length: int) -> list:
        """Рекурсивно генерирует дочерние узлы для родительского узла.

        Args:
            depth: Текущая глубина рекурсии.
            length: Количество дочерних узлов.

        Returns:
            generated_nodes (list): Список сгенерированных дочерних узлов.

        Algorithm:
            1. Вероятность терминального узла растет квадратично с глубиной
            2. Для нетерминальных узлов выбирается случайная операция
            3. Рекурсия продолжается до достижения max_depth
        """
        parents = []
        len1, len2 = len(nodes[1]), len(nodes[2])

        for _ in range(length):
            # Вероятность терминального узла зависит от глубины
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

    def operate(self, x: float, y: float) -> float:
        """Вычисляет значение дерева для заданных x и y.

        Args:
            x: Значение переменной x.
            y: Значение переменной y.

        Returns:
            result (float): Результат вычисления математического выражения.

        Raises:
            AttributeError: Если дерево не инициализировано (root is None).
        """
        if self.root is None:
            raise AttributeError("Дерево не инициализировано. Вызовите random() сначала.")
        return self.root.operate(x, y)

    def get_function_string(self) -> str:
        """Возвращает строковое представление математического выражения.

        Returns:
            expression (str): Строка с формулой в читаемом формате.

        Raises:
            AttributeError: Если дерево не инициализировано (root is None).
        """
        if self.root is None:
            raise AttributeError("Дерево не инициализировано. Вызовите random() сначала.")
        return self.root.get_func_string()
