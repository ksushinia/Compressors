def rle_encode(data):
    if not data:
        return []

    encoding = []
    prev_char = data[0]
    count = 1

    print(f"Начало кодирования. Первый символ: '{prev_char}'")

    for char in data[1:]:
        print(f"Текущий символ: '{char}', предыдущий: '{prev_char}'")
        if char == prev_char:
            count += 1
            print(f"Символы совпадают. Увеличиваем счётчик до {count}")
        else:
            encoding.append((prev_char, count))
            print(f"Символы не совпадают. Добавляем пару: ('{prev_char}', {count})")
            prev_char = char
            count = 1
            print(f"Начинаем новую последовательность с символа '{prev_char}'")

    encoding.append((prev_char, count))
    print(f"Конец данных. Добавляем последнюю пару: ('{prev_char}', {count})")
    return encoding

def rle_decode(encoded):
    decoded = ''
    for char, count in encoded:
        decoded += char * count
        print(f"Декодируем пару: ('{char}', {count}). Результат: '{decoded}'")
    return decoded

# Пример использования
data = "AAAABBBCCDAA"
print(f"Исходные данные: '{data}'")

encoded = rle_encode(data)
print(f"Закодированные данные: {encoded}")

decoded = rle_decode(encoded)
print(f"Декодированные данные: '{decoded}'")