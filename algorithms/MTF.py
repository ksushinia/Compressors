def mtf_encode(input_string):
    # Инициализация списка символов
    symbol_list = list(range(256))  # Список символов от 0 до 255 (ASCII)

    encoded_output = []

    print("Начальный список символов:", symbol_list[:10], "...")  # Выводим первые 10 символов для наглядности

    for i, char in enumerate(input_string):
        # Находим индекс символа в списке
        index = symbol_list.index(ord(char))

        # Добавляем индекс в выходной список
        encoded_output.append(index)

        # Перемещаем символ в начало списка
        symbol_list.pop(index)
        symbol_list.insert(0, ord(char))

        # Выводим промежуточные данные
        print(f"\nШаг {i + 1}: Символ '{char}' (ASCII: {ord(char)})")
        print(f"Индекс в списке: {index}")
        print(f"Список символов после перемещения: {symbol_list[:10]} ...")

    print("\nЗакодированный список:", encoded_output)
    return encoded_output


def mtf_decode(encoded_list):
    # Инициализация списка символов
    symbol_list = list(range(256))  # Список символов от 0 до 255 (ASCII)

    decoded_output = []

    print("Начальный список символов:", symbol_list[:10], "...")  # Выводим первые 10 символов для наглядности

    for i, index in enumerate(encoded_list):
        # Получаем символ по индексу
        char = chr(symbol_list[index])

        # Добавляем символ в выходной список
        decoded_output.append(char)

        # Перемещаем символ в начало списка
        symbol_list.pop(index)
        symbol_list.insert(0, ord(char))

        # Выводим промежуточные данные
        print(f"\nШаг {i + 1}: Индекс {index}")
        print(f"Символ: '{char}' (ASCII: {ord(char)})")
        print(f"Список символов после перемещения: {symbol_list[:10]} ...")

    decoded_string = ''.join(decoded_output)
    print("\nДекодированная строка:", decoded_string)
    return decoded_string


# Пример использования
input_string = "banana"
print("Исходная строка:", input_string)

# Кодирование
print("\n=== Кодирование ===")
encoded = mtf_encode(input_string)

# Декодирование
print("\n=== Декодирование ===")
decoded_string = mtf_decode(encoded)