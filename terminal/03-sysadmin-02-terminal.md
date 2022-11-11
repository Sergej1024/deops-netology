## Домашнее задание к занятию "3.2. Работа в терминале, лекция 2"

### 1. Какого типа команда cd? Попробуйте объяснить, почему она именно такого типа; опишите ход своих мыслей, если считаете что она могла бы быть другого типа

 Строго говоря, это вообще никакая не утилита. Ее нет в файловой системе. Это встроенная команда Bash и меняет текущую папку только для оболочки, в которой выполняется.

### 2. Какая альтернатива без pipe команде grep <some_string> <some_file> | wc -l? man grep поможет в ответе на этот вопрос. Ознакомьтесь с документом о других подобных некорректных вариантах использования pipe

```shell
[vagrant@centos8 ~]$ cat tst_bash
fgjksbfkg;bgkdb
kjdgbjlgbled
12378245
[vagrant@centos8 ~]$ grep 12378245 tst_bash | wc -l
1
[vagrant@centos8 ~]$ grep 12378245 tst_bash -c
1
 Useless Use of Wc -l
This is my personal favorite. There is actually a whole class of "Useless Use of (something) | grep (something) | (something)" problems but this one usually manifests itself in scripts riddled by useless backticks and pretzel logic.

Anything that looks like

     something | grep '..*' | wc -l

can usually be rewritten like something along the lines of

     something | grep -c .   # Notice that . is better than '..*'
```

### 3. Какой процесс с PID 1 является родителем для всех процессов в вашей виртуальной машине Ubuntu 20.04?

```shell
systemd(1)─┬─NetworkManager(905)─┬─{NetworkManager}(908)
           │                     └─{NetworkManager}(910)
           ├─VBoxService(1117)─┬─{VBoxService}(1118)
           │                   ├─{VBoxService}(1119)
           │                   ├─{VBoxService}(1121)
           │                   ├─{VBoxService}(1122)
           │                   ├─{VBoxService}(1123)
           │                   ├─{VBoxService}(1125)
           │                   ├─{VBoxService}(1126)
           │                   └─{VBoxService}(1127)
           ├─agetty(929)
           ├─auditd(803)───{auditd}(804)
           ├─chronyd(849)
           ├─crond(923)
           ├─dbus-daemon(833)───{dbus-daemon}(852)
           ├─firewalld(875)───{firewalld}(1021)
           ├─haveged(708)
           ├─irqbalance(827)───{irqbalance}(835)
           ├─polkitd(830)─┬─{polkitd}(863)
           │              ├─{polkitd}(864)
           │              ├─{polkitd}(868)
           │              ├─{polkitd}(869)
           │              └─{polkitd}(873)
           ├─rsyslogd(1027)─┬─{rsyslogd}(1033)
           │                └─{rsyslogd}(1034)
           ├─sshd(979)───sshd(37694)───sshd(37697)───bash(37698)───pstree(38096)
           ├─sssd(828)─┬─sssd_be(859)
           │           └─sssd_nss(872)
           ├─systemd(37616)───(sd-pam)(37619)
           ├─systemd-journal(710)
           ├─systemd-logind(891)
           ├─systemd-udevd(707)
           └─tuned(914)─┬─{tuned}(955)
                        ├─{tuned}(959)
                        ├─{tuned}(963)
                        └─{tuned}(965)
```

### 4. Как будет выглядеть команда, которая перенаправит вывод stderr ls на другую сессию терминала?

Вызов из pts/0:

```shell
ls -l 2>/dev/pts/1
```

### 5. Получится ли одновременно передать команде файл на stdin и вывести ее stdout в другой файл? Приведите работающий пример

```shell
[vagrant@centos8 ~]$ cat tst_bash
fgjksbfkg;bgkdb
kjdgbjlgbled
12378245
[vagrant@centos8 ~]$ cat tst_bash_out
cat: tst_bash_out: No such file or directory
[root@centos8 vagrant]#  cat <tst_bash >tst_bash_out
[root@centos8 vagrant]# cat tst_bash_out
fgjksbfkg;bgkdb
kjdgbjlgbled
12378245
```

### 6. Получится ли находясь в графическом режиме, вывести данные из PTY в какой-либо из эмуляторов TTY? Сможете ли вы наблюдать выводимые данные?

Да, сможем, надо перенаправить поток на tty

```shell
echo Hello, world! > /dev/tty2
```

### 7. Выполните команду bash 5>&1. К чему она приведет? Что будет, если вы выполните echo netology > /proc/$$/fd/5? Почему так происходит?

bash 5>&1 - Создаст дескриптор с 5 и перенатправит его в stdout
echo netology > /proc/$$/fd/5 - выведет в дескриптор "5", который был пернеаправлен в stdout

```shell
[root@centos8 vagrant]# bash 5>&1
[root@centos8 vagrant]# echo netology > /proc/$$/fd/5
netology
[root@centos8 vagrant]#
```

### 8. Получится ли в качестве входного потока для pipe использовать только stderr команды, не потеряв при этом отображение stdout на pty? Напоминаем: по умолчанию через pipe передается только stdout команды слева от | на stdin команды справа. Это можно сделать, поменяв стандартные потоки местами через промежуточный новый дескриптор, который вы научились создавать в предыдущем вопросе

```shell
[root@centos8 vagrant]# ls -l /root 7>&2 2>&1 1>&7 |grep denied -c
total 0
0
```

- 7>&2 - новый дескриптор перенаправили в stderr
- 2>&1 - stderr перенаправили в stdout
- 1>&7 - stdout - перенаправили в новый дескриптор

### 9. Что выведет команда cat /proc/$$/environ? Как еще можно получить аналогичный по содержанию вывод?

Переменные окружения оболочки, их также можно получить с помощью команд env, printenv

### 10. Используя man, опишите что доступно по адресам /proc/<PID>/cmdline, /proc/<PID>/exe

- /proc/<PID>/cmdline - полный путь до исполняемого файла процесса [PID]  (строка 231)
- /proc/<PID>/exe - содержит ссылку до файла запущенного для процесса [PID], cat выведет содержимое запущенного файла, запуск этого файла,  запустит еще одну копию самого файла  (строка 285)

### 11. Узнайте, какую наиболее старшую версию набора инструкций SSE поддерживает ваш процессор с помощью /proc/cpuinfo

sse 4.2

### 12. При открытии нового окна терминала и vagrant ssh создается новая сессия и выделяется pty. Это можно подтвердить командой tty, которая упоминалась в лекции 3.2. Однако

```shell
vagrant@netology1:~$ ssh localhost 'tty'
not a tty
```

Почитайте, почему так происходит, и как изменить поведение.

```shell
[vagrant@centos8 ~]$ ssh localhost 'tty'
The authenticity of host 'localhost (127.0.0.1)' can't be established.
RSA key fingerprint is SHA256:gMgAdx4zBi0Vw2RAc7p8MFi2v9ywt6GKMJikau5Af/E.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'localhost' (RSA) to the list of known hosts.
vagrant@localhost: Permission denied (publickey,gssapi-keyex,gssapi-with-mic).
```

но с локальной машины выдает так

```shell
 [root@homesrv ~]#  ssh localhost 'tty'
The authenticity of host 'localhost (::1)' can't be established.
ECDSA key fingerprint is SHA256:QLP2BaHZ78GbBnbkDI2AQSKuWlyQmQWvq+9K8bzdlPU.
ECDSA key fingerprint is MD5:45:77:ad:39:29:15:60:dd:ce:04:32:04:be:3a:99:4b.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'localhost' (ECDSA) to the list of known hosts.
root@localhost's password:
не телетайп
```

   если добавить параметр -t то получится так, команда принудительно создаст псевдопользователя

```shell
[root@homesrv ~]#  ssh -t localhost 'tty'
root@localhost's password:
/dev/pts/1
Connection to localhost closed.   
```

### 13. Бывает, что есть необходимость переместить запущенный процесс из одной сессии в другую. Попробуйте сделать это, воспользовавшись reptyr. Например, так можно перенести в screen процесс, который вы запустили по ошибке в обычной SSH-сессии

   Пререквизиты: есть reptyrи tmux/ screen установлены; Вы сможете найти их с apt-get или yum, в зависимости от вашей платформы.

    Используйте Ctrl+, Z чтобы приостановить процесс.

    Возобновите процесс в фоновом режиме с bg

    Найдите идентификатор процесса фонового процесса с помощью jobs -l

    Вы увидите нечто похожее на это:

    [1]+ 11475 Stopped (signal) yourprocessname

    Отключить работу от текущего родителя (оболочки) с disown yourprocessname

    Начало tmux(предпочтительно) или screen.

    Снова подключите процесс к tmux/ screenсеансу с reptyr:

    reptyr 11475

    Теперь вы можете отсоединить мультиплексор (по умолчанию Ctrl+ B, D для tmuxили Ctrl+ A, D для screen) и отключить SSH, пока ваш процесс продолжается в tmux/ screen.

    Позже, когда вы снова подключитесь к SSH, вы сможете подключиться к мультиплексору (например tmux attach).

### 14. sudo echo string > /root/new_file не даст выполнить перенаправление под обычным пользователем, так как перенаправлением занимается процесс shell'а, который запущен без sudo под вашим пользователем. Для решения данной проблемы можно использовать конструкцию echo string | sudo tee /root/new_file. Узнайте что делает команда tee и почему в отличие от sudo echo команда с sudo tee будет работать

команда tee делает вывод одновременно и в файл, указаный в качестве параметра, и в stdout, в данном примере команда получает вывод из stdin, перенаправленный через pipe от stdout команды echo и так как команда запущена от sudo , соотвественно имеет права на запись в файл
