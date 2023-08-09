import asyncio
import os
import random
import string


def random_string_generator(size, chars=string.ascii_lowercase + string.digits):
    """Генерим код, для отправки пользователю"""
    return ''.join(random.choice(chars) for _ in range(size))

def send_message():
    import time
    time.sleep(2)