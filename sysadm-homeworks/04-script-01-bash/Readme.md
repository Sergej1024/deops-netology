## Домашнее задание к занятию "4.1. Командная оболочка Bash: Практические навыки"

1.  Есть скрипт:
```shell
    a=1
    b=2
    c=a+b
    d=$a+$b
    e=$(($a+$b))
```
    
- Какие значения переменным c,d,e будут присвоены?
- Почему?

```shell
user@home MINGW64 ~/PycharmProjects/devops-netology
$ a=1

user@home MINGW64 ~/PycharmProjects/devops-netology
$ b=2

user@home MINGW64 ~/PycharmProjects/devops-netology
$ c=a+b

user@home MINGW64 ~/PycharmProjects/devops-netology
$ echo $c
a+b

user@home MINGW64 ~/PycharmProjects/devops-netology
$ d=$a+$b

user@home MINGW64 ~/PycharmProjects/devops-netology
$ echo $d
1+2

user@home MINGW64 ~/PycharmProjects/devops-netology
$ e=$(($a+$b))

user@home MINGW64 ~/PycharmProjects/devops-netology
$ echo $e
3
```
- c = "a+b" - так как указали текст а не переменные
- d = "1+2" - команда преобразовала вывела значения переменных, но не выполнила арифметическйо операции так как по умолчанию это строки 
- e = "3"   - так как теперь за счет скобок мы дали команду на выполнение арифметической операции со значениями переменных 

2.    На нашем локальном сервере упал сервис и мы написали скрипт, который постоянно проверяет его доступность, записывая дату проверок до тех пор, пока сервис не станет доступным. В скрипте допущена ошибка, из-за которой выполнение не может завершиться, при этом место на Жёстком Диске постоянно уменьшается. Что необходимо сделать, чтобы его исправить:
```shell
    while ((1==1)
    do
    curl https://localhost:4757
    if (($? != 0))
    then
    date >> curl.log
    fi
    done
```
    1. в условии _**while ((1==1)**_ нехватате закрывающей скобки )
    2. слишком частые проверки забивают файл, нужно добавить sleep - для задания интервала проверки
    3. нужно добавить проверку успешности чтоб выйти из цикла
       например: else exit
```shell
     while (( 1 == 1 ))
    do
        curl https://localhost:4757
        if (($? != 0))
        then
            date >> curl.log
        else exit
        fi
        sleep 5
    done    
```
3.   Необходимо написать скрипт, который проверяет доступность трёх IP: 192.168.0.1, 173.194.222.113, 87.250.250.242 по 80 порту и записывает результат в файл log. Проверять доступность необходимо пять раз для каждого узла.
```shell
[root@homesrv ~]cat check_hosts.sh
hosts=(192.168.0.1 173.194.222.113 87.250.250.24)
timeout=5
for i in {1..5}
do
date >>hosts.log
    for h in ${hosts[@]}
    do
        curl -Is --connect-timeout $timeout $h:80 >/dev/null
        echo "    check" $h status=$? >>hosts.log
    done
done
[root@homesrv ~]# ./check_hosts.sh
[root@homesrv ~]# cat hosts.log
Вс мар  6 17:53:22 +05 2022
    check 192.168.0.1 status=7
    check 173.194.222.113 status=0
    check 87.250.250.24 status=28
Вс мар  6 17:53:30 +05 2022
Вс мар  6 17:58:52 +05 2022
    check 192.168.0.1 status=7
    check 173.194.222.113 status=0
    check 87.250.250.24 status=28
Вс мар  6 17:59:00 +05 2022
    check 192.168.0.1 status=7
    check 173.194.222.113 status=0
    check 87.250.250.24 status=28
Вс мар  6 17:59:09 +05 2022
    check 192.168.0.1 status=7
    check 173.194.222.113 status=0
    check 87.250.250.24 status=28
Вс мар  6 17:59:17 +05 2022
    check 192.168.0.1 status=7
    check 173.194.222.113 status=0
Вс мар  6 18:01:08 +05 2022
    check 192.168.0.1 status=7
    check 173.194.222.113 status=0
    check 87.250.250.24 status=28
Вс мар  6 18:01:16 +05 2022
    check 192.168.0.1 status=7
    check 173.194.222.113 status=0
    check 87.250.250.24 status=28
Вс мар  6 18:01:25 +05 2022
    check 192.168.0.1 status=7
    check 173.194.222.113 status=0
    check 87.250.250.24 status=28
Вс мар  6 18:01:33 +05 2022
    check 192.168.0.1 status=7
    check 173.194.222.113 status=0
    check 87.250.250.24 status=28
Вс мар  6 18:01:41 +05 2022
    check 192.168.0.1 status=7
    check 173.194.222.113 status=0
    check 87.250.250.24 status=28
[root@homesrv ~]#    
```
4. Необходимо дописать скрипт из предыдущего задания так, чтобы он выполнялся до тех пор, пока один из узлов не окажется недоступным. Если любой из узлов недоступен - IP этого узла пишется в файл error, скрипт прерывается

добавил в начало скрипта таймаут на ожидания коннекта для курла в цикле укажем выполнять пока переменная res = 0 (в которую запишем результат curl)
```shell
[root@homesrv ~]# cat check_host2.sh
hosts=(192.168.0.1 173.194.222.113 87.250.250.24)
timeout=5
res=0

while (($res == 0))
do
    for h in ${hosts[@]}
    do
        curl -Is --connect-timeout $timeout $h:80 >/dev/null
        res=$?
        if (($res != 0))
        then
            echo "    ERROR on " $h status=$res >>hosts2.log
        fi
    done
done
[root@homesrv ~]# ./check_host2.sh
[root@homesrv ~]# cat hosts2.log
    ERROR on  192.168.0.1 status=7
    ERROR on  87.250.250.24 status=28
[root@homesrv ~]#
```