import numpy as np
import queue
import time
import math

class Node():
    def __init__(self, symbol=None, counter=None, left=None, right=None, parent=None):
        self.symbol = symbol
        self.counter = counter
        self.left = left
        self.right = right
        self.parent = parent

    def __lt__(self, other):
        return self.counter < other.counter

def count_symb(data: bytes) -> np.ndarray:
    counter = np.zeros(256, dtype=int)
    for byte in data:
        counter[byte] += 1
    return counter

def huffman_compress(data: bytes) -> bytes:
    C = count_symb(data)
    list_of_leafs = []
    Q = queue.PriorityQueue()

    for i in range(256):
        if C[i] != 0:
            leaf = Node(symbol=i, counter=C[i])
            list_of_leafs.append(leaf)
            Q.put(leaf)

    while Q.qsize() >= 2:
        left_node = Q.get()
        right_node = Q.get()
        parent_node = Node(left=left_node, right=right_node)
        left_node.parent = parent_node
        right_node.parent = parent_node
        parent_node.counter = left_node.counter + right_node.counter
        Q.put(parent_node)

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

    coded_message = ""
    for byte in data:
        coded_message += codes[byte]

    padding = 8 - len(coded_message) % 8
    coded_message += '0' * padding
    coded_message = f"{padding:08b}" + coded_message

    bytes_string = bytearray()
    for i in range(0, len(coded_message), 8):
        byte = coded_message[i:i + 8]
        bytes_string.append(int(byte, 2))

    return bytes(bytes_string), codes

def huffman_decompress(compressed_data: bytes, huffman_codes: dict) -> bytes:
    padding = compressed_data[0]
    coded_message = ""
    for byte in compressed_data[1:]:
        coded_message += f"{byte:08b}"

    if padding > 0:
        coded_message = coded_message[:-padding]

    reverse_codes = {v: k for k, v in huffman_codes.items()}
    current_code = ""
    decoded_data = bytearray()

    for bit in coded_message:
        current_code += bit
        if current_code in reverse_codes:
            decoded_data.append(reverse_codes[current_code])
            current_code = ""

    return bytes(decoded_data)

def read_huffman_codes(codes_file):
    huffman_codes = {}
    with open(codes_file, 'r') as f:
        for line in f:
            symbol, code = line.strip().split(':')
            huffman_codes[int(symbol)] = code
    return huffman_codes

def write_huffman_codes(huffman_codes, file_path):
    with open(file_path, 'w') as code_file:
        for symbol, code in huffman_codes.items():
            code_file.write(f"{symbol}:{code}\n")

def calculate_entropy(data: bytes) -> float:
    """
    Вычисляет энтропию данных по формуле Шеннона.
    """
    counter = count_symb(data)
    total_symbols = len(data)
    entropy = 0.0

    for count in counter:
        if count > 0:
            probability = count / total_symbols
            entropy -= probability * math.log2(probability)

    return entropy

def calculate_average_code_length(huffman_codes: dict, data: bytes) -> float:
    """
    Вычисляет среднюю длину кода Хаффмана.
    """
    counter = count_symb(data)
    total_symbols = len(data)
    total_length = 0.0

    for symbol, code in huffman_codes.items():
        probability = counter[symbol] / total_symbols
        total_length += probability * len(code)

    return total_length

def process_file_nontext_1(file_path, output_compressed, output_decompressed):

    start_time = time.time()

    # Чтение исходных данных
    with open(file_path, "rb") as f:
        data = f.read()
    original_size = len(data)
    print(f"Исходный размер данных: {original_size} байт")

    # Сжатие данных
    compressed_bytes, huffman_codes = huffman_compress(data)
    compressed_size = len(compressed_bytes)
    print(f"Размер сжатых данных: {compressed_size} байт")

    # Запись сжатых данных и кодов Хаффмана
    with open(output_compressed, "wb") as file:
        file.write(compressed_bytes)

    with open(output_compressed + '_codes', 'w') as code_file:
        for symbol, code in huffman_codes.items():
            code_file.write(f"{symbol}:{code}\n")

    # Чтение сжатых данных и декомпрессия
    with open(output_compressed, "rb") as f:
        compressed_data = f.read()

    huffman_codes = read_huffman_codes(output_compressed + '_codes')
    decompressed_data = huffman_decompress(compressed_data, huffman_codes)
    decompressed_size = len(decompressed_data)
    print(f"Размер после декомпрессии: {decompressed_size} байт")

    # Вычисление коэффициента сжатия
    compression_ratio = original_size / compressed_size
    print(f"Коэффициент сжатия: {compression_ratio:.2f}")

    # Вычисление энтропии и средней длины кода
    entropy = calculate_entropy(data)
    avg_code_length = calculate_average_code_length(huffman_codes, data)
    print(f"Энтропия: {entropy:.2f} бит/символ")
    print(f"Средняя длина кода: {avg_code_length:.2f} бит/символ \n")

    # Запись декомпрессированных данных
    with open(output_decompressed, "wb") as file:
        file.write(decompressed_data)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Время выполнения: {elapsed_time:.2f} секунд")

# Список файлов для обработки
file_paths = [
    "C:/Users/79508/Desktop/4 семестри/АИСД/1 лабораторная/коди/буквы и картинки/text.txt",
    "C:/Users/79508/Desktop/4 семестри/АИСД/1 лабораторная/коди/буквы и картинки/binary_file.bin",
    "C:/Users/79508/Desktop/4 семестри/АИСД/1 лабораторная/коди/буквы и картинки/bw_image.raw",
    "C:/Users/79508/Desktop/4 семестри/АИСД/1 лабораторная/коди/буквы и картинки/gray_image.raw",
    "C:/Users/79508/Desktop/4 семестри/АИСД/1 лабораторная/коди/буквы и картинки/color_image.raw",
    "C:/Users/79508/Desktop/4 семестри/АИСД/1 лабораторная/коди/буквы и картинки/enwik7"
]

# Обработка каждого файла
for i, file_path in enumerate(file_paths):
    output_compressed = f"compressed_file_HA_{i+1}.bin"
    output_decompressed = f"decompressed_file_HA_{i+1}.bin"
    print(f"Обработка файла {file_path}...")
    process_file_nontext_1(file_path, output_compressed, output_decompressed)