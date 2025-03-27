import queue

# Класс для узла дерева Хаффмана
class Node:
    def __init__(self, symbol=None, counter=0, left=None, right=None):
        self.symbol = symbol
        self.counter = counter
        self.left = left
        self.right = right
        self.parent = None

    def __lt__(self, other):
        return self.counter < other.counter

# Подсчет частот символов
def count_symb(S):
    C = [0] * 128  # Для ASCII символов
    for s in S:
        C[ord(s)] += 1
    return C

# Визуализация дерева Хаффмана (рекурсивно)
def print_tree(node, indent="", is_left=True):
    if node is None:
        return
    print(indent, end="")
    if is_left:
        print("├── ", end="")
        indent += "│   "
    else:
        print("└── ", end="")
        indent += "    "
    print(f"({node.symbol if node.symbol else 'Internal'}, {node.counter})")
    print_tree(node.left, indent, True)
    print_tree(node.right, indent, False)

# Статический алгоритм Хаффмана
def HA(S):
    if not S:
        return b"", {}

    # Подсчет частот символов
    C = count_symb(S)
    print("Частоты символов:")
    for i in range(128):
        if C[i] != 0:
            print(f"'{chr(i)}': {C[i]}")

    list_of_leafs = []
    Q = queue.PriorityQueue()

    # Создание узлов для каждого символа
    for i in range(128):
        if C[i] != 0:
            leaf = Node(symbol=chr(i), counter=C[i])
            list_of_leafs.append(leaf)
            Q.put(leaf)

    # Построение дерева Хаффмана
    while Q.qsize() >= 2:
        left_node = Q.get()
        right_node = Q.get()
        parent_node = Node(left=left_node, right=right_node)
        left_node.parent = parent_node
        right_node.parent = parent_node
        parent_node.counter = left_node.counter + right_node.counter
        Q.put(parent_node)

    # Генерация кодов Хаффмана
    codes = {}
    for leaf in list_of_leafs:
        node = leaf
        code = ""
        while node.parent is not None:
            if node.parent.left == node:
                code = "0" + code
            else:
                code = "1" + code
            node = node.parent
        codes[leaf.symbol] = code

    print("\nТаблица кодов Хаффмана:")
    for symbol, code in codes.items():
        print(f"'{symbol}': {code}")

    # Кодирование строки
    coded_message = ""
    for s in S:
        coded_message += codes[s]

    print("\nЗакодированная строка до дополнения нулями:")
    print(coded_message)

    # Дополнение нулями до длины, кратной 8
    k = 8 - len(coded_message) % 8
    coded_message += "0" * k

    print("\nЗакодированная строка после дополнения нулями:")
    print(coded_message)

    # Преобразование в байты
    bytes_string = b""
    for i in range(0, len(coded_message), 8):
        s = coded_message[i:i+8]
        x = string_binary_to_int(s)
        bytes_string += x.to_bytes(1, "big")

    # Вывод коэффициента сжатия
    original_size = len(S)
    compressed_size = len(bytes_string)
    compression_ratio = original_size / compressed_size if compressed_size != 0 else 0
    print(f"\nКоэффициент сжатия: {compression_ratio:.2f}")

    # Вывод средней длины кода
    total_length = sum(len(code) for code in codes.values())
    avg_length = total_length / len(codes)
    print(f"Средняя длина кода: {avg_length:.2f}")

    # Визуализация дерева Хаффмана
    print("\nДерево Хаффмана:")
    root = Q.get()  # Корень дерева
    print_tree(root)

    return bytes_string, codes

# Преобразование строки из нулей и единиц в число
def string_binary_to_int(s):
    return int(s, 2)

# Пример использования
S = "abracadabra"
print("алгоритм HA")
print(f"Исходная строка: '{S}'")
encoded_data, codes = HA(S)
print("\nЗакодированные данные (в байтах):", encoded_data)