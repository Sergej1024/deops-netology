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
