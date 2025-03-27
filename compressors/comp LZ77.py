import time

# Функция для кодирования данных с помощью алгоритма LZ77
def lz77_encode(data: bytes, buffer_size: int) -> bytes:
    encoded_data = bytearray()
    i = 0
    n = len(data)

    while i < n:
        max_length = 0
        max_offset = 0

        # Определяем границы поиска
        search_start = max(0, i - buffer_size)
        search_end = i

        # Ищем максимальное совпадение
        for length in range(min(255, n - i), 0, -1):
            substring = data[i:i + length]
            offset = data[search_start:search_end].rfind(substring)
            if offset != -1:
                max_length = length
                max_offset = search_end - search_start - offset
                break

        if max_length > 0:
            # Кодируем offset и length в два байта каждый
            encoded_data.append((max_offset >> 8) & 0xFF)  # Старший байт offset
            encoded_data.append(max_offset & 0xFF)  # Младший байт offset
            encoded_data.append((max_length >> 8) & 0xFF)  # Старший байт length
            encoded_data.append(max_length & 0xFF)  # Младший байт length
            i += max_length
        else:
            # Если совпадений нет, кодируем как символ
            encoded_data.append(0)  # offset = 0 (старший байт)
            encoded_data.append(0)  # offset = 0 (младший байт)
            encoded_data.append(0)  # length = 0 (старший байт)
            encoded_data.append(0)  # length = 0 (младший байт)
            encoded_data.append(data[i])  # символ (1 байт)
            i += 1

    return bytes(encoded_data)


def lz77_decode(encoded_data: bytes) -> bytes:
    decoded_data = bytearray()
    i = 0
    n = len(encoded_data)

    while i < n:
        # Читаем offset и length (по два байта каждый)
        offset = (encoded_data[i] << 8) | encoded_data[i + 1]
        length = (encoded_data[i + 2] << 8) | encoded_data[i + 3]
        i += 4

        if offset == 0 and length == 0:
            # Это символ
            decoded_data.append(encoded_data[i])
            i += 1
        else:
            # Это ссылка
            start = len(decoded_data) - offset
            end = start + length
            decoded_data.extend(decoded_data[start:end])

    return bytes(decoded_data)


# Функция для обработки файла с использованием LZ77
def process_file_with_lz77(file_path, output_compressed, output_decompressed, buffer_size=1024):
    start_time = time.time()

    # Чтение исходных данных
    with open(file_path, "rb") as f:
        data = f.read()
    original_size = len(data)
    print(f"Исходный размер данных: {original_size} байт")

    # Сжатие данных с использованием LZ77
    compressed_bytes = lz77_encode(data, buffer_size)
    compressed_size = len(compressed_bytes)
    print(f"Размер сжатых данных: {compressed_size} байт")

    # Запись сжатых данных
    with open(output_compressed, "wb") as file:
        file.write(compressed_bytes)

    # Чтение сжатых данных и декомпрессия
    with open(output_compressed, "rb") as f:
        compressed_data = f.read()

    decompressed_data = lz77_decode(compressed_data)
    decompressed_size = len(decompressed_data)
    print(f"Размер после декомпрессии: {decompressed_size} байт")

    # Вычисление коэффициента сжатия
    compression_ratio = original_size / compressed_size
    print(f"Коэффициент сжатия: {compression_ratio:.2f}")

    # Запись декомпрессированных данных
    with open(output_decompressed, "wb") as file:
        file.write(decompressed_data)

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
    output_compressed = f"compressed_file_LZ77{i + 1}.bin"
    output_decompressed = f"decompressed_file_LZ77{i + 1}.bin"
    print(f"Обработка файла {file_path}...")
    process_file_with_lz77(file_path, output_compressed, output_decompressed)