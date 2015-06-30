#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import re
import json
from HTMLParser import HTMLParser

# Массив данных для POST запросов
post_data = dict()

# Парсер полей input из HTML
class FormInputParser(HTMLParser):
 def handle_starttag(self, tag, attrs):
  if (tag == 'input'):
   tag_params = dict(attrs)
   post_data[tag_params['name']] = tag_params['value']

# Попытка установить соединение с заданным сервером
def try_connect(address):
 try:
  requests.get(address, timeout=5)
 except requests.exceptions.ConnectionError:
  return(False)
 else:
  return(True)


# Функция авторизации
def connect():
 # Пока не разобрался с сессиями, будет хранилище header'ов
 headers={}
 
 # Получаем перенаправление
 page_vmetro = requests.get('http://vmet.ro')
 headers.update({'referer': page_vmetro.url})
 
 # Вытаскиваем назначение редиректа
 url_auth = re.search(
  'http:[^\"]*',
  page_vmetro.text
 ).group(0)
 
 # Запрашиваем страницу с кнопкой авторизации
 page_auth = requests.get(
 	url_auth,
 	headers=headers,
 	cookies=page_vmetro.cookies
 )
 headers.update({'referer': page_auth.url})
 
 # Парсим поля скрытой формы
 parser = FormInputParser()
 parser.feed(page_auth.text)
 
 # Отправляем полученную форму
 page_postauth = requests.post(
  url_auth,
  data=post_data,
  cookies=page_auth.cookies,
  headers=headers
 )
 headers.update({'referer': page_postauth.url})
 
 # Парсим поля второй скрытой формы
 parser.feed(page_postauth.text)
 
 # Отправляем окончательный запрос
 page_router = requests.post(
 	'http://1.1.1.1/login.html',
 	data=post_data,
 	cookies=page_postauth.cookies,
 	headers=headers
 )
 

def main():
 # "Пингуем" роутер
 if try_connect("http://1.1.1.1/login.html"):
  for counter in range(3):
   # HTTPS не позволяет провайдеру влезть с редиректом
   if try_connect("https://wtfismyip.com/text"):
    break
    
   connect()

if __name__ == "__main__":
 main()
