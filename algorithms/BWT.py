import numpy

def BWT(S):
    N = len(S)
    # Создаем все циклические сдвиги
    BWM = [S[i:] + S[:i] for i in range(N)]
    print("=== Все циклические сдвиги ===")
    for i, row in enumerate(BWM):
        print(f"{i}: {row}")
    # Сортируем сдвиги
    BWM_sorted = sorted(BWM)
    print("\n=== Отсортированные циклические сдвиги ===")
    for i, row in enumerate(BWM_sorted):
        print(f"{i}: {row}")
    # Получаем последний столбец
    last_column_BWM = ''.join(row[-1] for row in BWM_sorted)
    # Находим индекс исходной строки
    S_index = BWM_sorted.index(S)
    return last_column_BWM, S_index

def better_iBWT(last_column_BWM, S_index):
    N = len(last_column_BWM)
    P_inverse = counting_sort_arg(last_column_BWM)
    S = []
    j = S_index
    for _ in range(N):
        j = P_inverse[j]
        S.append(last_column_BWM[j])
    return ''.join(S)

def counting_sort_arg(S):
    N = len(S)
    M = 128
    T = [0] * M
    for s in S:
        T[ord(s)] += 1
    T_sub = [0] * M
    for j in range(1, M):
        T_sub[j] = T_sub[j-1] + T[j-1]
    P_inverse = [0] * N
    for i in range(N):
        P_inverse[T_sub[ord(S[i])]] = i
        T_sub[ord(S[i])] += 1
    return P_inverse

def count_symb(S):
    counter = numpy.zeros(128, dtype=int)
    for s in S:
        counter[ord(s)] += 1
    return counter

def prob_estimate(S):
    counter = count_symb(S)
    return counter / len(S)

def entropy(S):
    P = prob_estimate(S)
    P = P[P != 0]
    return -numpy.sum(P * numpy.log2(P))

# Исходная строка
S = "banana"
print(f"Исходная строка: {S}\n")

# Прямое преобразование BWT
bwt_result, index = BWT(S)
print(f"\nПрямое преобразование BWT: {bwt_result}, индекс: {index}")

# Обратное преобразование BWT
original_string = better_iBWT(bwt_result, index)
print(f"\nОбратное преобразование BWT: {original_string}")

# Проверка, что мы вернулись к исходной строке
assert original_string == S, "Ошибка: обратное преобразование BWT не совпадает с исходной строкой"