def lz78_compress(input_string):
    dictionary = {}
    current_string = ""
    output = []
    index = 1

    for symbol in input_string:
        combined_string = current_string + symbol
        if combined_string in dictionary:
            current_string = combined_string
        else:
            if current_string:
                output.append((dictionary[current_string], symbol))
            else:
                output.append((0, symbol))
            dictionary[combined_string] = index
            index += 1
            current_string = ""

    if current_string:
        output.append((dictionary[current_string], ''))

    return output, dictionary

def lz78_decompress(compressed_data):
    dictionary = {0: ''}
    index = 1
    decompressed_string = ""

    for (dict_index, symbol) in compressed_data:
        phrase = dictionary.get(dict_index, '') + symbol
        decompressed_string += phrase
        dictionary[index] = phrase
        index += 1

    return decompressed_string

# Пример использования
input_string = "abacabacabadaca"
compressed, dictionary = lz78_compress(input_string)
print("Сжатые данные:", compressed)
print("Словарь:", dictionary)

decompressed_string = lz78_decompress(compressed)
print("Распакованная строка:", decompressed_string)
def lz78_compress_with_logs(input_string):
    dictionary = {}
    current_string = ""
    output = []
    index = 1

    for symbol in input_string:
        combined_string = current_string + symbol
        if combined_string in dictionary:
            current_string = combined_string
            print(f"Найдена подстрока в словаре: '{combined_string}', продолжаем поиск.")
        else:
            if current_string:
                output.append((dictionary[current_string], symbol))
                print(f"Добавлена новая запись в словарь: '{combined_string}' с индексом {index}.")
            else:
                output.append((0, symbol))
                print(f"Добавлена новая запись в словарь: '{symbol}' с индексом {index}.")
            dictionary[combined_string] = index
            index += 1
            current_string = ""

    if current_string:
        output.append((dictionary[current_string], ''))
        print(f"Добавлена последняя запись в словарь: '{current_string}' с индексом {index}.")

    return output, dictionary

# Пример использования с логами
input_string = "abacabacabadaca"
compressed, dictionary = lz78_compress_with_logs(input_string)
print("Сжатые данные:", compressed)
print("Словарь:", dictionary)

decompressed_string = lz78_decompress(compressed)
print("Распакованная строка:", decompressed_string)