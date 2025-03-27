import numpy as np
import time
import math
import os

def count_symb(data: bytes) -> np.ndarray:
    """
    Подсчитывает частоту символов в данных.
    """
    counter = np.zeros(256, dtype=int)
    for byte in data:
        counter[byte] += 1
    return counter

def improved_rle_compress(data: bytes) -> bytes:
    """
    Сжимает данные с использованием улучшенного алгоритма RLE.
    """
    compressed_data = bytearray()
    n = len(data)
    i = 0

    while i < n:
        current_byte = data[i]
        count = 1

        # Подсчитываем количество повторений текущего байта
        while i + count < n and count < 255 and data[i + count] == current_byte:
            count += 1

        if count > 1:
            # Если последовательность повторяющаяся, записываем количество и байт
            compressed_data.append(count)
            compressed_data.append(current_byte)
            i += count
        else:
            # Если последовательность неповторяющаяся, собираем все неповторяющиеся символы
            non_repeating = bytearray()
            while i < n and (i + 1 >= n or data[i] != data[i + 1]):
                non_repeating.append(data[i])
                i += 1
                if len(non_repeating) == 255:
                    break
            # Записываем количество неповторяющихся символов и сами символы
            compressed_data.append(0)  # Флаг для неповторяющихся символов
            compressed_data.append(len(non_repeating))
            compressed_data.extend(non_repeating)

    return bytes(compressed_data)

def improved_rle_decompress(compressed_data: bytes) -> bytes:
    """
    Декомпрессия данных, сжатых с использованием улучшенного RLE.
    """
    decompressed_data = bytearray()
    n = len(compressed_data)
    i = 0

    while i < n:
        flag = compressed_data[i]
        if flag == 0:
            # Если флаг 0, это неповторяющаяся последовательность
            length = compressed_data[i + 1]
            decompressed_data.extend(compressed_data[i + 2:i + 2 + length])
            i += 2 + length
        else:
            # Если флаг не 0, это повторяющаяся последовательность
            count = flag
            byte = compressed_data[i + 1]
            decompressed_data.extend([byte] * count)
            i += 2

    return bytes(decompressed_data)

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

def calculate_average_code_length(data: bytes, compressed_data: bytes) -> float:
    """
    Вычисляет среднюю длину кода для RLE.
    """
    total_symbols = len(data)
    total_compressed_symbols = len(compressed_data)
    return (total_compressed_symbols * 8) / total_symbols  # В битах на символ

def process_file_nontext_1(file_path, output_compressed, output_decompressed):
    # Начало измерения времени
    start_time = time.time()

    # Чтение исходных данных
    with open(file_path, "rb") as f:
        data = f.read()
    original_size = len(data)
    print(f"Исходный размер данных: {original_size} байт")

    # Сжатие данных
    compressed_bytes = improved_rle_compress(data)
    compressed_size = len(compressed_bytes)
    print(f"Размер сжатых данных: {compressed_size} байт")

    # Запись сжатых данных
    with open(output_compressed, "wb") as file:
        file.write(compressed_bytes)

    # Чтение сжатых данных и декомпрессия
    with open(output_compressed, "rb") as f:
        compressed_data = f.read()

    decompressed_data = improved_rle_decompress(compressed_data)
    decompressed_size = len(decompressed_data)
    print(f"Размер после декомпрессии: {decompressed_size} байт")

    # Запись декомпрессированных данных
    with open(output_decompressed, "wb") as file:
        file.write(decompressed_data)

    # Вычисление коэффициента сжатия
    compression_ratio = original_size / compressed_size
    print(f"Коэффициент сжатия: {compression_ratio:.2f}")

    # Вычисление энтропии
    entropy = calculate_entropy(data)
    print(f"Энтропия: {entropy:.2f} бит/символ")

    # Вычисление средней длины кода
    avg_code_length = calculate_average_code_length(data, compressed_bytes)
    print(f"Средняя длина кода: {avg_code_length:.2f} бит/символ")

    # Конец измерения времени
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Время выполнения: {elapsed_time:.2f} секунд \n")


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
    output_compressed = f"compressed_file_RLE_{i+1}.bin"
    output_decompressed = f"decompressed_file_RLE_{i+1}.bin"
    print(f"Обработка файла {file_path}...")
    process_file_nontext_1(file_path, output_compressed, output_decompressed)