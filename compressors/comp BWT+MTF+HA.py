import numpy as np
import heapq
import time
import math
import os
from collections import defaultdict

# Размер блока (200 КБ)
BLOCK_SIZE = 200 * 1024


# Класс для узлов дерева Хаффмана
class HuffmanNode:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


# Функции для BWT
def bwt_transform(data: bytes, chunk_size: int = 1024) -> tuple[bytes, list[int]]:
    transformed_data = bytearray()
    indices = []
    for start in range(0, len(data), chunk_size):
        chunk = data[start:start + chunk_size]
        index, encoded_chunk = transform_chunk(chunk)
        transformed_data.extend(encoded_chunk)
        indices.append(index)
    return bytes(transformed_data), indices


def transform_chunk(chunk: bytes) -> tuple[int, bytes]:
    rotations = [chunk[i:] + chunk[:i] for i in range(len(chunk))]
    rotations.sort()
    original_index = rotations.index(chunk)
    encoded_chunk = bytes(rotation[-1] for rotation in rotations)
    return original_index, encoded_chunk


def bwt_inverse(transformed_data: bytes, indices: list[int], chunk_size: int = 1024) -> bytes:
    restored_data = bytearray()
    position = 0
    index = 0
    while position < len(transformed_data):
        end = position + chunk_size if position + chunk_size <= len(transformed_data) else len(transformed_data)
        chunk = transformed_data[position:end]
        original_index = indices[index]
        restored_chunk = reverse_transform_chunk(original_index, chunk)
        restored_data.extend(restored_chunk)
        position = end
        index += 1
    return bytes(restored_data)


def reverse_transform_chunk(original_index: int, encoded_chunk: bytes) -> bytes:
    table = [(char, idx) for idx, char in enumerate(encoded_chunk)]
    table.sort()
    result = bytearray()
    current_row = original_index
    for _ in range(len(encoded_chunk)):
        char, current_row = table[current_row]
        result.append(char)
    return bytes(result)


# Функции для MTF
def mtf_transform(data: bytes) -> bytes:
    alphabet = list(range(256))
    transformed_data = bytearray()
    for byte in data:
        index = alphabet.index(byte)
        transformed_data.append(index)
        alphabet.pop(index)
        alphabet.insert(0, byte)
    return bytes(transformed_data)


def mtf_inverse(transformed_data: bytes) -> bytes:
    alphabet = list(range(256))
    original_data = bytearray()
    for index in transformed_data:
        byte = alphabet[index]
        original_data.append(byte)
        alphabet.pop(index)
        alphabet.insert(0, byte)
    return bytes(original_data)


# Функции для Хаффмана
def build_huffman_tree(freq_dict):
    heap = []
    for char, freq in freq_dict.items():
        heapq.heappush(heap, HuffmanNode(char=char, freq=freq))

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(freq=left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)

    return heapq.heappop(heap)


def build_huffman_codes(node, current_code="", codes=None):
    if codes is None:
        codes = {}
    if node.char is not None:
        codes[node.char] = current_code
    else:
        build_huffman_codes(node.left, current_code + "0", codes)
        build_huffman_codes(node.right, current_code + "1", codes)
    return codes

def huffman_compress(data: bytes) -> tuple[bytes, dict]:
    freq_dict = defaultdict(int)
    for byte in data:
        freq_dict[byte] += 1

    if len(freq_dict) == 0:
        return bytes(), {}

    root = build_huffman_tree(freq_dict)
    codes = build_huffman_codes(root)

    encoded_bits = []
    for byte in data:
        encoded_bits.append(codes[byte])

    bit_string = ''.join(encoded_bits)
    padding = 8 - len(bit_string) % 8
    bit_string += '0' * padding

    compressed = bytearray()
    compressed.append(padding)

    for i in range(0, len(bit_string), 8):
        byte = bit_string[i:i + 8]
        compressed.append(int(byte, 2))

    return bytes(compressed), codes


def huffman_decompress(compressed_data: bytes, huffman_codes: dict) -> bytes:
    if len(compressed_data) == 0:
        return bytes()

    padding = compressed_data[0]
    bit_string = ''.join(f"{byte:08b}" for byte in compressed_data[1:])
    if padding > 0:
        bit_string = bit_string[:-padding]

    reverse_codes = {v: k for k, v in huffman_codes.items()}
    current_code = ""
    decompressed = bytearray()

    for bit in bit_string:
        current_code += bit
        if current_code in reverse_codes:
            decompressed.append(reverse_codes[current_code])
            current_code = ""

    return bytes(decompressed)


def process_block(block: bytes) -> tuple[bytes, list[int], dict, float, float]:
    # BWT
    transformed_data, indices = bwt_transform(block)

    # MTF
    transformed_data = mtf_transform(transformed_data)

    # Huffman
    compressed_data, codes = huffman_compress(transformed_data)

    return compressed_data, indices, codes


def compress_file(file_path, output_compressed):
    start_time = time.time()

    with open(file_path, "rb") as f:
        data = f.read()
    original_size = len(data)
    print(f"Обработка файла {file_path}...")
    print(f"Исходный размер данных: {original_size} байт")

    total_entropy = 0.0
    total_avg_code_length = 0.0
    block_count = 0

    with open(output_compressed, "wb") as compressed_file:
        with open(file_path, "rb") as f:
            block_number = 0
            while True:
                block = f.read(BLOCK_SIZE)
                if not block:
                    break

                compressed_block, indices, codes = process_block(block)
                block_count += 1

                compressed_file.write(block_number.to_bytes(4, 'big'))
                compressed_file.write(len(indices).to_bytes(4, 'big'))
                for index in indices:
                    compressed_file.write(index.to_bytes(4, 'big'))

                code_bytes = serialize_huffman_codes(codes)
                compressed_file.write(len(code_bytes).to_bytes(4, 'big'))
                compressed_file.write(code_bytes)

                compressed_file.write(len(compressed_block).to_bytes(4, 'big'))
                compressed_file.write(compressed_block)
                block_number += 1

    compressed_size = os.path.getsize(output_compressed)
    print(f"Размер сжатых данных: {compressed_size} байт")

    compression_ratio = original_size / compressed_size if compressed_size > 0 else 0
    print(f"Коэффициент сжатия: {compression_ratio:.2f}")

    end_time = time.time()
    print(f"Время выполнения: {end_time - start_time:.2f} секунд")


def decompress_file(input_compressed, output_decompressed):
    start_time = time.time()

    with open(input_compressed, "rb") as f:
        blocks = {}
        while True:
            block_number_bytes = f.read(4)
            if not block_number_bytes:
                break

            block_number = int.from_bytes(block_number_bytes, 'big')
            num_indices = int.from_bytes(f.read(4), 'big')
            indices = [int.from_bytes(f.read(4), 'big') for _ in range(num_indices)]

            code_size = int.from_bytes(f.read(4), 'big')
            code_bytes = f.read(code_size)
            codes = deserialize_huffman_codes(code_bytes)

            block_size = int.from_bytes(f.read(4), 'big')
            compressed_block = f.read(block_size)

            # Huffman декомпрессия
            decompressed_transformed = huffman_decompress(compressed_block, codes)

            # MTF декомпрессия
            decompressed_transformed = mtf_inverse(decompressed_transformed)

            # BWT декомпрессия
            decompressed_data = bwt_inverse(decompressed_transformed, indices)
            blocks[block_number] = decompressed_data

    with open(output_decompressed, "wb") as decompressed_file:
        for block_number in sorted(blocks.keys()):
            decompressed_file.write(blocks[block_number])

    decompressed_size = os.path.getsize(output_decompressed)
    print(f"Размер после декомпрессии: {decompressed_size} байт\n")


def serialize_huffman_codes(codes):
    serialized = bytearray()
    for char, code in codes.items():
        serialized.extend([char, len(code)])
        code_bytes = int(code, 2).to_bytes((len(code) + 7) // 8, 'big')
        serialized.append(len(code_bytes))
        serialized.extend(code_bytes)
    return bytes(serialized)


def deserialize_huffman_codes(code_bytes):
    codes = {}
    i = 0
    while i < len(code_bytes):
        char = code_bytes[i]
        code_len = code_bytes[i + 1]
        bytes_len = code_bytes[i + 2]
        i += 3

        code_int = int.from_bytes(code_bytes[i:i + bytes_len], 'big')
        code = bin(code_int)[2:].zfill(code_len)
        codes[char] = code
        i += bytes_len
    return codes


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
    output_compressed = f"compressed_BWT+MTF+HA_{i + 1}.bin"
    output_decompressed = f"decompressed_BWT+MTF+HA_{i + 1}.bin"

    # Сжатие
    compress_file(file_path, output_compressed)

    # Распаковка
    decompress_file(output_compressed, output_decompressed)