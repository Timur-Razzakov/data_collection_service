from random import randint

""" Функция для рандомного вывода user_agent-тов"""


def random_agent():
    user_agent = []
    with open("user_agent_list.txt", "r") as f:
        text = f.readlines()
        for line in text:
            user_agent.append(line)

    headers = [
        {'User-Agent': f'{user_agent[randint(0, 984)]}',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    ]
    return headers

from user_agent import random_agent
# user_agent
header = str(random_agent())
