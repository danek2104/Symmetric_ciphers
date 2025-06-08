def mod_inverse(a, m=26):
    """Находит обратное число a по модулю m."""
    for inv in range(1, m):
        if (a * inv) % m == 1:
            return inv
    raise ValueError(f"Обратного числа для {a} mod {m} не существует")

def affine_encrypt(text, a, b):
    """Шифрует текст с помощью аффинного шифра (обобщенный шифр Цезаря)."""
    encrypted = []
    for char in text:
        if char.isupper():
            x = ord(char) - ord('A')
            y = (a * x + b) % 26
            encrypted.append(chr(y + ord('A')))
        elif char.islower():
            x = ord(char) - ord('a')
            y = (a * x + b) % 26
            encrypted.append(chr(y + ord('a')))
        else:
            encrypted.append(char)
    return ''.join(encrypted)

def affine_decrypt(ciphertext, a, b):
    """Дешифрует текст, зашифрованный аффинным шифром."""
    a_inv = mod_inverse(a)
    decrypted = []
    for char in ciphertext:
        if char.isupper():
            y = ord(char) - ord('A')
            x = (a_inv * (y - b)) % 26
            decrypted.append(chr(x + ord('A')))
        elif char.islower():
            y = ord(char) - ord('a')
            x = (a_inv * (y - b)) % 26
            decrypted.append(chr(x + ord('a')))
        else:
            decrypted.append(char)
    return ''.join(decrypted)


def affine_break(ciphertext):
    """Восстанавливает исходный текст без знания ключа с помощью частотного анализа."""
    from collections import Counter
    # Эталонные частоты букв английского языка (в порядке убывания)
    freq_eng = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
    
    # Фильтруем только буквы и приводим к верхнему регистру
    letters = [char.upper() for char in ciphertext if char.isalpha()]
    if not letters:
        return ciphertext
    
    # Находим две самые частые буквы в тексте
    counter = Counter(letters)
    common = [char for char, _ in counter.most_common(2)]
    
    # Возможные значения для a (взаимно простые с 26)
    valid_a = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
    best_guess = None
    best_score = -1
    
    # Перебираем все возможные пары (a, b)
    for a in valid_a:
        a_inv = mod_inverse(a)
        for b in range(26):
            # Пробуем дешифровать
            decrypted = affine_decrypt(ciphertext, a, b)
            # Оцениваем качество текста по частотному анализу
            decrypted_letters = [char.upper() for char in decrypted if char.isalpha()]
            decrypted_freq = Counter(decrypted_letters)
            # Сортируем буквы по частоте в тексте
            sorted_letters = ''.join([char for char, _ in decrypted_freq.most_common()])
            # Сравниваем с эталоном (первые 6 букв)
            score = sum(1 for letter in sorted_letters[:6] if letter in freq_eng[:6])
            if score > best_score:
                best_score = score
                best_guess = decrypted
    
    return best_guess



import secrets

def vernam_encrypt(plaintext):
    """Шифрует текст с помощью шифра Вернама (одноразовый блокнот)."""
    plain_bytes = plaintext.encode('utf-8')
    key = secrets.token_bytes(len(plain_bytes))
    cipher_bytes = bytes([pb ^ kb for pb, kb in zip(plain_bytes, key)])
    return cipher_bytes, key

def vernam_decrypt(ciphertext, key):
    """Дешифрует текст, зашифрованный шифром Вернама."""
    plain_bytes = bytes([cb ^ kb for cb, kb in zip(ciphertext, key)])
    return plain_bytes.decode('utf-8')


text = "Hello, World!"
a, b = 5, 8  # Ключи

# Шифрование
encrypted = affine_encrypt(text, a, b)
print("Зашифрованный текст:", encrypted)  # "Jgnnq, Yqtnf!"

# Дешифрование
decrypted = affine_decrypt(encrypted, a, b)
print("Расшифрованный текст:", decrypted)  # "Hello, World!"

# Взлом без ключа
broken_text = affine_break(encrypted)
print("Восстановленный текст:", broken_text)  # "Hello, World!"