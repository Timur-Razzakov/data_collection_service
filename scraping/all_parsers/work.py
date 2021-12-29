# import requests
# import codecs
# from bs4 import BeautifulSoup as BS
# from random import randint
#
# user_agent = []
# with open("scraping/all_parsers/user_agent_list.txt", "r") as f:
#     text = f.readlines()
#     for line in text:
#         user_agent.append(line)
#
# headers = [
#     {'User-Agent': f'{user_agent[randint(0, 984)]}',
#      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
# ]
#
#
# def work(url, city=None, speciality=None):
#     jobs_info = []
#     errors = []
#     domain = 'https://www.work.ua'
#     if url:
#         resp = requests.get(url, headers)
#
#         if resp.status_code == 200:
#             soup = BS(resp.content, 'html.parser')
#             main_div = soup.find('div', id='pjax-job-list')
#             if main_div:
#                 div_lst = main_div.find_all('div', attrs={'class': 'job-link'})
#                 for div in div_lst:
#                     title = div.find('h2')
#                     # salary = 'з/п не указана'
#                     salary = div.select('div:nth-child(3) > b')
#                     if not salary:
#                         salary = 'з/п не указана'
#                     else:
#                         print(type(salary))
#                         salary = (list(salary))
#                         print(type(salary))
#                         print(salary)
#                     # if salary_found:
#                     #     salary = salary_found
#                     href = title.a['href']
#                     content = div.p.text
#                     company = 'No name'
#                     logo = div.find('img')
#                     if logo:
#                         company = logo['alt']
#                     jobs_info.append({'title': title.text, 'url': domain + href,
#                                       'description': content, 'company': company,
#                                       'city_id': city, 'salary': salary, 'speciality_id': speciality})
#             else:
#                 errors.append({'url': url, 'title': "Div does not exists"})
#         else:
#             errors.append({'url': url, 'title': "Page do not response"})
#
#     return jobs_info, errors
#
#
# print(work('https://www.work.ua/ru/jobs-kyiv-python/', ))