# def matrh_test(a, b):
#
#     res = [a + b, a - b, a * b, a / b, a // b, a % b, (a ** 5 + b ** 5)]
#     print(res)
#     for item in res:
#         print(type(item))
#     b = "\n".join(res)
#     return b
# print(matrh_test(3, 8))

# def flavia(n, k):
#     return k + 1
#
#
# print(flavia(498, 68))
# def math_test(a, b):
#     res = (a + b, a - b, a * b, a / b, a // b, a % b, pow((a ** 10 + b ** 10),1/2),)
#
#     print( '\n'.join([str(item) for item in res]))
# print(math_test(3, 8))
from os import remove

from icecream import ic


#
# number = input()
# if len(number) <= 5:
#     number = list(number.rstrip('0'))
#     number.reverse()
#     print(''.join(number))
# else:
#     number = list(number)
#     num = number[-5:]
#     remainder = number[0:-5]
#     num.reverse()
#     res = remainder + num
#     print(''.join(res))


# number = input()
# print(int(number[:-5] + number[-5:][::-1]))
# """
# Необходимо написать программу, реализующую алгоритм написания этой песни.
# Алгоритм выводит в конце предложения следующую в алфавитном порядке букву,
# если она встречается в строке текста, а очередную строку отображает уже без этой буквы.
#
# """
# word = input() + ' запретил букву'
# b = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
#      'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
# # alpha = [chr(i) for i in range(1072, 1104)]
# for item in b:

#     if item in word:
#         print(word, item)
#         word = word.translate({ord(i): None for i in item}).replace('  ', ' ').strip()  # удаление букв из предложения

# def funcc(func):
#     print('text')
#     func()
#     return funcc
#
#
# @funcc
# def res():
#     text = 56465465
#     print(text)
# res('sdfsdfsdf')