#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import re
import json
import datetime
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
  'https?:[^\"]*',
  page_vmetro.text
 ).group(0)
 
 # Запрашиваем страницу с кнопкой авторизации
 page_auth = requests.get(
  url_auth,
  headers=headers,
  cookies=page_vmetro.cookies,
  verify=False
 )
 headers.update({'referer': page_auth.url})
 
 # Парсим поля скрытой формы
 parser = FormInputParser()
 parser.feed(re.search("<body>.*?</body>", page_auth.content, re.DOTALL).group(0))
 
 # Отправляем полученную форму
 page_postauth = requests.post(
  url_auth,
  data=post_data,
  cookies=page_auth.cookies,
  headers=headers,
  verify=False
 )

def main():
 print(datetime.datetime.now())

 # "Пингуем" роутер
 if try_connect("http://1.1.1.1/login.html"):
  for counter in range(3):
   # HTTPS не позволяет провайдеру влезть с редиректом
   if try_connect("https://wtfismyip.com/text"):
    if counter == 0:
     print("Already connected")
    else:
     print("Connected")
    
    break
   
   try:
    connect()
   except requests.exceptions.ConnectionError:
    print("Connection failed")
 
 else:
  print("Wrong network")

if __name__ == "__main__":
 main()
