## Домашнее задание к занятию "4.3. Языки разметки JSON и YAML"

### 1. Мы выгрузили JSON, который получили через API запрос к нашему сервису:
```json
{ "info" : "Sample JSON output from our service\t",
        "elements" :[
            { "name" : "first",
            "type" : "server",
            "ip" : 7175 
            },
            { "name" : "second",
            "type" : "proxy",
            "ip : 71.78.22.43
            }
        ]
    }
```
Нужно найти и исправить все ошибки, которые допускает наш сервис

Пропущены ковычки у ip адреса
```json
{ "info" : "Sample JSON output from our service\t",
        "elements" :[
            { "name" : "first",
            "type" : "server",
            "ip" : 7175 
            },
            { "name" : "second",
            "type" : "proxy",
            "ip" : "71.78.22.43"
            }
        ]
    }
```

### 2. В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. К уже реализованному функционалу нам нужно добавить возможность записи JSON и YAML файлов, описывающих наши сервисы. Формат записи JSON по одному сервису: { "имя сервиса" : "его IP"}. Формат записи YAML по одному сервису: - имя сервиса: его IP. Если в момент исполнения скрипта меняется IP у сервиса - он должен так же поменяться в yml и json файле.
```python
##!/usr/bin/env python3
from typing import Any

import socket as s
import time as t
import datetime as dt
import json
import yaml

i = 1
wait = 2  # интервал проверок в секундах
srv = {'drive.google.com': '0.0.0.0', 'mail.google.com': '0.0.0.0', 'google.com': '0.0.0.0'}
init = 0
f_conf = "/home/sergej/python/"  # путь к файлам конфигов
f_log = "/home/sergej/python/error.log"  # путь к файлам логов

print('*' * 37 + "start script" + '*' * 37)
print(srv)
print('*' * 86)

while True: #1 == 1:  # отладочное число проверок
    for host in srv:
        is_error = False
        ip = s.gethostbyname(host)
        if ip != srv[host]:
            if i == 1 and init != 1:
                is_error = True
                with open(f_log, 'a') as fl:
                    print(
                        str(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ' [ERROR] ' +
                        str(host) + ' IP mistmatch: ' + srv[host] + ' ' + ip, file=fl)
                # json
                with open(f_conf + host + ".json", 'w') as jsf:
                    json_data = json.dumps({host: ip})
                    jsf.write(json_data)
                # yaml
                with open(f_conf + host + ".yaml", 'w') as ymf:
                    yaml_data = yaml.dump([{host: ip}])
                    ymf.write(yaml_data)
            srv[host] = ip
    # счетчик итераций для отладки, закомментировать для бесконечного цикла 3 строки
    i += 1
    if i >= 40:
        break
    t.sleep(wait)
```