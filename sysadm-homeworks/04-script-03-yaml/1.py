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

while True:  #1 == 1:  # отладочное число проверок
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
                # в один общий файл
                if is_error:
                    data = []
                    for host in srv:
                        data.append({host: ip})
                    with open(f_conf + "services_conf.json", 'w') as jsf:
                        json_data = json.dumps(data)
                        jsf.write(json_data)
                    with open(f_conf + "services_conf.yaml", 'w') as ymf:
                        yaml_data = yaml.dump(data)
                        ymf.write(yaml_data)
            srv[host] = ip
    # счетчик итераций для отладки, закомментировать для бесконечного цикла 3 строки
    i += 1
    if i >= 40:
        break
    t.sleep(wait)
