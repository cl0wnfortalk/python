import math
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


# теорема Пифагора для нахождения гипотенузы, прилежащего и противоположного катетов 

class Trigonometry:
    """ Pythagorean theorem for hypotenuse (c), leg (b) and leg(a) """

    def hypot(self, a, b):
        """ Solve for hypotenuse """
        return math.sqrt(a**2 + b ** 2)
    
    def leg_b(self, a, c):
        """ Solve for leg b """
        return math.sqrt(c ** 2 - a ** 2)
    
    def leg_a(self, b, c):
        """ Solve for leg a """
        return math.sqrt(c ** 2 - b ** 2)

# Многоалфавитные подстановки - базовая криптография

import re

class CipherMatrix:

    """Реализация многоалфавитных подстановок
    Для замены символов исходного текста используется 
    не один, а несколько алфавитов. Алфавиты 
    для замены образованы из символов исходного 
    алфавита, записанных в другом порядке."""

    __langs = {
        "ru":list('АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'),
        "en":list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
    }

    def __lang_protection(self, text, lang):
        if not re.fullmatch(r'[А-Я]', text) and re.fullmatch(r'[A-Z]', text):
            raise self.CipherMatrixException(f"Строка '{text}' не соответствует {lang} либо использован нижний регистр")

    class CipherMatrixException(Exception):
        """Кастомное исключение для CipherMatrix"""
        pass

    @classmethod
    def __get_cipher_matrix(self, key:str, lang="ru"):

        """Возвращает список строк алфавита
        В первой строке матрицы записывают буквы в 
        порядке очередности их в исходном алфавите, 
        во второй — ту же последовательность букв, 
        но с циклическим сдвигом влево на одну позицию, 
        в третьей — со сдвигом на две позиции"""

        if not isinstance(key, str):
            raise TypeError(f"key argument must be string, not {type(key)}")

        if len(key) == 0:
            raise ValueError("Empty key found")

        if len(key) < 3:
            print("Предупреждение: оптимальная длина ключа должна превышать 2 символа")
            is_ok = str(input("'Y' чтобы продолжить: ")).lower()
            if is_ok != "y":
                return None
                        
        al = self.__langs.get(lang) if self.__langs.get(lang) else None 

        if al is None:
            raise self.CipherMatrixException(f"Only {self.__langs.keys()} are allowed, not {lang}")
            
        mtrx = ["".join(al)]

        for char in key:
            try:
                char_index = al.index(char) 
            except ValueError:
                raise self.CipherMatrixException(f"'{char}' отсутствует в заданном алфавите - {lang}")
            mtrx.append("".join(al[char_index:] + al[:char_index]))
        return mtrx

    @classmethod
    def encode_with_mtrx(self, text:str, key:str, textlang="ru"):

        """Шифрование тескста через матрицу шифрования по ключу"""

        if not isinstance(text, str):
            raise TypeError(f"text argument must be string but {type(text)} is used")

        if len(text) == 0:
            raise ValueError("text argument should not be empty")
        
        self.__lang_protection(self, text, textlang)
        
        cipher_table = self.__get_cipher_matrix(key, textlang)

        al = self.__langs.get(textlang)
        count = 0
        secret = ""
        for char in text:
            if char == " ": 
                secret += " "
                continue
            try:
                index = al.index(char)
            except ValueError:
                raise self.CipherMatrixException(f"'{char}' отсутствует в заданном алфавите - {textlang}")
            letter = cipher_table[1:][count][index]
            count += 1
            if count >= len(cipher_table[1:]):
                count = 0
            secret += letter
        return secret
    
    @classmethod
    def decode_with_mtrx(self, cipher:str, key:str, textlang:str):
        
        """Дешифрование зашифрованного текста с ключом"""

        if not isinstance(cipher, str):
            raise TypeError(f"text argument must be string but {type(cipher)} is used")

        if len(cipher) == 0:
            raise ValueError("text argument should not be empty")
        
        self.__lang_protection(self, cipher, textlang)

        
        cipher_table = self.__get_cipher_matrix(key, textlang)

        al = self.__langs.get(textlang)
        count = 0
        nonsecret = ""
        for char in cipher:
            if char == " ": 
                nonsecret += " "
                continue
            index = cipher_table[1:][count].index(char)
            try:
                letter = al[index]
            except ValueError:
                raise self.CipherMatrixException(f"'{char}' отсутствует в заданном алфавите - {textlang}")
            count += 1
            if count >= len(cipher_table[1:]):
                count = 0
            nonsecret += letter
        return nonsecret



secret = CipherMatrix.encode_with_mtrx("PROTECTION", "WINTER", "en")
nonsecret = CipherMatrix.decode_with_mtrx(secret, "WINTER", "en")
print(secret)
print(nonsecret)
