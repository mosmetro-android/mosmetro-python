# Wi-Fi в метро (python-версия)

Данный скрипт позволяет автоматизировать подключение к интернету в сетях москосвкого (и не только) общественного транспорта. Скрипт написан на Python 2.x, что позволяет запускать его не только на компьютерах, но и на мобильных устройствах.

## Поддерживаемые алгоритмы

В данный момент поддерживается только алгоритм MosMetroV2, созданный компанией МаксимаТелеком и являющийся наиболее распространённым в сетях общественного транспорта в Москве и других городах России. Если вы видите сеть с названием MT_FREE, то этот скрипт в 99% случаев вам подойдёт.

Алгоритм постоянно изменяется, так что скрипт может перестать работать в любой момент. Также провайдер предпринимает меры против пользователей оригинального приложения и этого скрипта, поэтому не исключено получение блокировки (пока временной).

## Зависимости

* Python 2.x или 3.x
* [requests](https://pypi.python.org/pypi/requests)
* [pyquery](https://pypi.python.org/pypi/pyquery)
* [fake-useragent](https://pypi.python.org/pypi/fake-useragent) (необязательно)

### Установка через pip

```
sudo apt-get install python-pip
sudo pip install -r requirements.txt
```

## Использование

Для авторизации в сети MT_FREE просто запустите скрипт. Он сам определит совместимость с текущей сетью и при отсутствии доступа в интернет попытается авторизовать данное устройство.

```
python app.py
```

Примечание: При первом подключении устройства всё-же необходимо пройти авторизацию через SMS или ГосУслуги для регистрации именно этого устройства в сети. После этого скрипт будет нормально работать.

### Автоматизация на Android

Запуск данного скрипта можно автоматизировать в Android при помощи двух программ: QPython (в качестве исполняющей среды Python) и Tasker (или любой программы, умеющей выполнять shell-команды автоматически). Подробнее об автоматизации на Android вы можете узнать <a href="http://thedrhax.pw/?p=1768">здесь</a>.

Для большей надёжности и более простой установки вы можете воспользоваться приложением [Wi-Fi в метро](https://github.com/mosmetro-android/mosmetro-android), которое использует тот же алгоритм, но в оптимизированном для Android виде.

### Автоматизация в Linux

Для автоматического запуска данного скрипта при подключении к сети можно скопировать файл *metro.py* в директорию */etc/network/if-up.d/* и сделать его исполняемым. Для этого вы можете воспользоваться следующими командами, запущенными с правами администратора:

```
cp app.py /etc/network/if-up.d/mosmetro-python.py
chmod +x /etc/network/if-up.d/mosmetro-python.py
```

Скрипт будет запускаться при подключении к любой сети, но это не является большой проблемой, так как перед полноценной попыткой подключения производится быстрая проверка на наличие поддерживаемой сети.

## Лицензия

Данный проект распространяется под лицензией GNU General Public License версии 3 или новее. Вы можете ознакомиться с полным текстом лицензии по [этой](./LICENSE) ссылке.

Исходный код предоставлен для ознакомления. Автор не несёт никакой ответственности за его использование и возможные нарушения Правил Пользования других сервисов.
