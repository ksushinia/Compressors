def lz77_compress(data, search_buffer_size=1024, look_ahead_buffer_size=256):
    i = 0
    compressed_data = []

    while i < len(data):
        # Определяем границы буферов
        search_buffer_start = max(0, i - search_buffer_size)
        search_buffer = data[search_buffer_start:i]
        look_ahead_buffer = data[i:i + look_ahead_buffer_size]

        # Ищем максимальное совпадение
        best_offset = 0
        best_length = 0
        best_char = '' if i >= len(data) else data[i]

        for offset in range(1, len(search_buffer) + 1):
            length = 0
            while (length < len(look_ahead_buffer) and
                   i - offset + length < len(data) and
                   data[i - offset + length] == data[i + length]):
                length += 1

            if length > best_length:
                best_offset = offset
                best_length = length
                best_char = '' if i + best_length >= len(data) else data[i + best_length]

        # Добавляем найденную тройку в сжатые данные
        compressed_data.append((best_offset, best_length, best_char))

        # Выводим текущий шаг на русском
        print(f"Шаг {len(compressed_data)}:")
        print(f"  Буфер поиска: '{search_buffer}'")
        print(f"  Буфер предпросмотра: '{look_ahead_buffer}'")
        print(f"  Наилучшее совпадение: (смещение={best_offset}, длина={best_length}, след.символ='{best_char}')")
        print(f"  Сжатые данные: {compressed_data}")
        print()

        # Сдвигаем окно
        i += best_length + 1

    return compressed_data


# Пример использования с русскоязычным выводом
print("алгоритм LZ77")
data = "abracadabra"
print(f"Исходные данные: '{data}'")
print("\nПроцесс сжатия:")
compressed = lz77_compress(data)
print("\nИтоговые сжатые данные:", compressed)