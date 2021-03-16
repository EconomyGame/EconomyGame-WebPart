import random
import string


def get_random_string(size=10):
    """Генерация рандомной строки из цифр и ascii символов длиной size"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(size))

