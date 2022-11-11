## Домашнее задание к занятию "4.2. Использование Python для решения типовых DevOps задач"

### 1. Есть скрипт:
```python
#!/usr/bin/env python3

a = 1
b = '2'
c = a + b
```
- Какое значение будет присвоено переменной c?

будет выведена ошибка TypeError: unsupported operand type(s) for +: 'int' and 'str'
- Как получить для переменной c значение 12?

```python
c=str(a)+b
print (c)
12
``` 
- Как получить для переменной c значение 3?

```python
c=a+int(b)
print (c)
3
```

###2. Мы устроились на работу в компанию, где раньше уже был DevOps Engineer. Он написал скрипт, позволяющий узнать, какие файлы модифицированы в репозитории, относительно локальных изменений. Этим скриптом недовольно начальство, потому что в его выводе есть не все изменённые файлы, а также непонятен полный путь к директории, где они находятся. Как можно доработать скрипт ниже, чтобы он исполнял требования вашего руководителя?
```python
#!/usr/bin/env python3

import os

bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(prepare_result)
        break
```
Доработанный скрипт
лишняя логическая переменная is_change
и команда break которая прерывает обработку при первом найденном вхождении
в вывод добавлен путь
```python
#!/usr/bin/env python3

import os

bash_command = ["cd ~/devops-netology", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
#is_change = False
for result in result_os.split('\n'):
    if result.find('изменено') != -1:
        prepare_result = result.replace('\tизменено:   ', '')
        print("~/devops-netology/" + prepare_result)
#        break
```
Вывод:
```shell
[sergej@surg-adm 04-script-02-py]$ ./2.py
~/devops-netology/   .idea/workspace.xml
~/devops-netology/   04-script-02-py/Readme.md

[sergej@surg-adm 04-script-02-py]$ git status
На ветке main
Ваша ветка обновлена в соответствии с «origin/main».

Изменения, которые будут включены в коммит:
  (используйте «git restore --staged <файл>…», чтобы убрать из индекса)
        новый файл:    Readme.md

Изменения, которые не в индексе для коммита:
  (используйте «git add <файл>…», чтобы добавить файл в индекс)
  (используйте «git restore <файл>…», чтобы отменить изменения в рабочем каталоге)
        изменено:      ../.idea/workspace.xml
        изменено:      Readme.md

```

###3. Доработать скрипт выше так, чтобы он мог проверять не только локальный репозиторий в текущей директории, а также умел воспринимать путь к репозиторию, который мы передаём как входной параметр. Мы точно знаем, что начальство коварное и будет проверять работу этого скрипта в директориях, которые не являются локальными репозиториями.

```python
#!/usr/bin/env python3

import os
import sys

cmd = os.getcwd()

if len(sys.argv)>=2:
    cmd = sys.argv[1]
bash_command = ["cd "+cmd, "git status 2>&1"]

print('\033[95m')
result_os = os.popen(' && '.join(bash_command)).read()
for result in result_os.split('\n'):
    if result.find('fatal') != -1:
        print('\033[31m Каталог \033[1m '+cmd+'\033[0m\033[31m не является GIT репозиторием\033[0m')    
    if result.find('изменено') != -1:
        prepare_result = result.replace('\tизменено: ', '')
        prepare_result = prepare_result.replace(' ', '')
        print(cmd+"/"+prepare_result)
print('\033[0m')
```

```pycon
[sergej@surg-adm 04-script-02-py]$ ./3.py

/home/sergej/devops-netology/04-script-02-py/../.idea/workspace.xml
/home/sergej/devops-netology/04-script-02-py/3.py
/home/sergej/devops-netology/04-script-02-py/Readme.md

[sergej@surg-adm /]$ /home/sergej/devops-netology/04-script-02-py/3.py

 Каталог  / не является GIT репозиторием

```

###4. Наша команда разрабатывает несколько веб-сервисов, доступных по http. Мы точно знаем, что на их стенде нет никакой балансировки, кластеризации, за DNS прячется конкретный IP сервера, где установлен сервис. Проблема в том, что отдел, занимающийся нашей инфраструктурой очень часто меняет нам сервера, поэтому IP меняются примерно раз в неделю, при этом сервисы сохраняют за собой DNS имена. Это бы совсем никого не беспокоило, если бы несколько раз сервера не уезжали в такой сегмент сети нашей компании, который недоступен для разработчиков. Мы хотим написать скрипт, который опрашивает веб-сервисы, получает их IP, выводит информацию в стандартный вывод в виде: <URL сервиса> - <его IP>. Также, должна быть реализована возможность проверки текущего IP сервиса c его IP из предыдущей проверки. Если проверка будет провалена - оповестить об этом в стандартный вывод сообщением: [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>. Будем считать, что наша разработка реализовала сервисы: drive.google.com, mail.google.com, google.com.
```python
##!/usr/bin/env python3

import socket as s
import time as t
import datetime as dt

i = 1
wait = 2  # интервал проверок в секундах
srv = {'drive.google.com': '0.0.0.0', 'mail.google.com': '0.0.0.0', 'google.com': '0.0.0.0'}
init = 0

print('*' * 37 + "start script" + '*' * 37)
print(srv)
print('*'*86)

while 1 == 1:  # отладочное число проверок
    for host in srv:
        ip = s.gethostbyname(host)
        if ip != srv[host]:
            if i == 1 and init != 1:
                print(
                    str(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ' [ERROR] ' + str(host) + ' IP mistmatch: ' +
                    srv[host] + ' ' + ip)
            srv[host] = ip
    # счетчик итераций для отладки, закомментировать для бесконечного цикла 3 строки
#    i += 1
#    if i >= 10:
#        break
    t.sleep(wait)
```
```pycon
*************************************start script*************************************
{'drive.google.com': '0.0.0.0', 'mail.google.com': '0.0.0.0', 'google.com': '0.0.0.0'}
**************************************************************************************
2022-03-13 17:44:34 [ERROR] drive.google.com IP mistmatch: 0.0.0.0 173.194.220.194
2022-03-13 17:44:34 [ERROR] mail.google.com IP mistmatch: 0.0.0.0 173.194.73.19
2022-03-13 17:44:34 [ERROR] google.com IP mistmatch: 0.0.0.0 209.85.233.102
2022-03-13 17:50:45 [ERROR] mail.google.com IP mistmatch: 173.194.73.19 173.194.73.18
2022-03-13 17:51:54 [ERROR] google.com IP mistmatch: 209.85.233.102 209.85.233.138
2022-03-13 17:53:32 [ERROR] drive.google.com IP mistmatch: 173.194.220.194 173.194.221.194
2022-03-13 17:54:08 [ERROR] google.com IP mistmatch: 209.85.233.138 108.177.14.139
2022-03-13 17:55:47 [ERROR] mail.google.com IP mistmatch: 173.194.73.18 173.194.73.17
```