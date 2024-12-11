""" algorithms """

# ==Сортировка слиянием (Merge Sort)==


def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    # Разделение массива на две половины
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    # Слияние отсортированных половин
    return merge(left_half, right_half)

def merge(left, right):
    sorted_array = []
    left_index, right_index = 0, 0

    # Слияние двух половин
    while left_index < len(left) and right_index < len(right):
        if left[left_index] < right[right_index]:
            sorted_array.append(left[left_index])
            left_index += 1
        else:
            sorted_array.append(right[right_index])
            right_index += 1

    # Добавление оставшихся элементов
    sorted_array.extend(left[left_index:])
    sorted_array.extend(right[right_index:])

    return sorted_array


# ==Быстрая сортировка==

def quick_sort(arr):
    # Если массив пустой или состоит из одного элемента, он уже отсортирован
    if len(arr) <= 1:
        return arr
    else:
        # Выбираем опорный элемент (в данном случае - последний элемент)
        pivot = arr[-1]
        left = []  # Элементы меньше опорного
        right = []  # Элементы больше опорного
        for item in arr[:-1]:  # Проходим по всем элементам, кроме опорного
            if item <= pivot:
                left.append(item)  # Добавляем в левую часть
            else:
                right.append(item)  # Добавляем в правую часть
        # Рекурсивно сортируем обе части и объединяем с опорным элементом
        return quick_sort(left) + [pivot] + quick_sort(right)
    

# ==Сортировка вставками (Insertion Sort)==

def insertion_sort(arr):
    # Проходим по всем элементам массива, начиная со второго
    for i in range(1, len(arr)):
        key = arr[i]  # Текущий элемент для вставки
        j = i - 1  # Индекс последнего элемента отсортированной части

        # Сдвигаем элементы, которые больше ключа, вправо
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]  # Сдвигаем элемент вправо
            j -= 1

        # Вставляем текущий элемент на его правильное место
        arr[j + 1] = key


# ==Сортировка пузырьком (Bubble Sort)==

def bubble_sort(arr):
    n = len(arr)
    # Проход по всем элементам массива
    for i in range(n):
        # Флаг для отслеживания необходимости дальнейших проходов
        swapped = False
        # Последние i элементов уже отсортированы
        for j in range(0, n - i - 1):
            # Сравниваем соседние элементы
            if arr[j] > arr[j + 1]:
                # Меняем местами, если они в неправильном порядке
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        # Если за проход ничего не поменялось, массив отсортирован
        if not swapped:
            break
    return arr


# АЛГОРИТМЫ ПОИСКА

# ==Бинарный поиск (Binary Search)==

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        # Проверяем, найден ли искомый элемент
        if arr[mid] == target:
            return mid  # Возвращаем индекс найденного элемента
        elif arr[mid] < target:
            left = mid + 1  # Искомый элемент может быть только в правой части
        else:
            right = mid - 1  # Искомый элемент может быть только в левой части
            
    return -1  # Элемент не найден


# ==Линейный поиск (Linear search)==

def linear_search(arr, target):
    """linear search algorithm"""
    for index, value in enumerate(arr):
        if value == target:
            return index
    return -1 

# МАТЕМАТИЧЕСКИЕ АЛГОРИТМЫ

def gcd(a, b):
    """Returns GCD of a and b"""
    while b != 0:
        a, b = b, a % b 
    return a  

def lcm(a, b):
    """Returns LCM of a and b"""
    return abs(a * b) // gcd(a, b)
