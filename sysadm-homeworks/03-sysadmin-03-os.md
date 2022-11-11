## Домашнее задание к занятию "3.3. Операционные системы, лекция 1"

### 1. Какой системный вызов делает команда cd? В прошлом ДЗ мы выяснили, что cd не является самостоятельной программой, это shell builtin, поэтому запустить strace непосредственно на cd не получится. Тем не менее, вы можете запустить strace на /bin/bash -c 'cd /tmp'. В этом случае вы увидите полный список системных вызовов, которые делает сам bash при старте. Вам нужно найти тот единственный, который относится именно к cd

```shell
newfstatat(AT_FDCWD, "/tmp", {st_mode=S_IFDIR|S_ISVTX|0777, st_size=520, ...}, 0) = 0
chdir("/tmp") 
```

### 2. Попробуйте использовать команду file на объекты разных типов на файловой системе. Например

```shell
    vagrant@netology1:~$ file /dev/tty
    /dev/tty: character special (5/0)
    vagrant@netology1:~$ file /dev/sda
    /dev/sda: block special (8/0)
    vagrant@netology1:~$ file /bin/bash
    /bin/bash: ELF 64-bit LSB shared object, x86-64
```

    Используя strace выясните, где находится база данных file на основании которой она делает свои догадки.
    
    Файл базы типов - /usr/share/misc/magic.mgc
    в тексте это:

```shell
    newfstatat(AT_FDCWD, "/home/sergej/.magic.mgc", 0x7ffc464fe630, 0) = -1 ENOENT (Нет такого файла или каталога)
    newfstatat(AT_FDCWD, "/home/sergej/.magic", 0x7ffc464fe630, 0) = -1 ENOENT (Нет такого файла или каталога)
    openat(AT_FDCWD, "/etc/magic.mgc", O_RDONLY) = -1 ENOENT (Нет такого файла или каталога)
    newfstatat(AT_FDCWD, "/etc/magic", {st_mode=S_IFREG|0644, st_size=111, ...}, 0) = 0
    openat(AT_FDCWD, "/etc/magic", O_RDONLY) = 3
    newfstatat(3, "", {st_mode=S_IFREG|0644, st_size=111, ...}, AT_EMPTY_PATH) = 0
    read(3, "# Magic local data for file(1) c"..., 4096) = 111
    read(3, "", 4096)                       = 0
    close(3)                                = 0
    openat(AT_FDCWD, "/usr/share/misc/magic.mgc", O_RDONLY) = 3
    newfstatat(3, "", {st_mode=S_IFREG|0644, st_size=6652944, ...}, AT_EMPTY_PATH) = 0
    mmap(NULL, 6652944, PROT_READ|PROT_WRITE, MAP_PRIVATE, 3, 0) = 0x7fd1eda3d000
```

### 3. Предположим, приложение пишет лог в текстовый файл. Этот файл оказался удален (deleted в lsof), однако возможности сигналом сказать приложению переоткрыть файлы или просто перезапустить приложение – нет. Так как приложение продолжает писать в удаленный файл, место на диске постепенно заканчивается. Основываясь на знаниях о перенаправлении потоков предложите способ обнуления открытого удаленного файла (чтобы освободить место на файловой системе)

```shell
    [sergej@surg-adm ~]$ lsof | grep /tmp/test1
    ping      301543                           sergej    1w      REG               0,35     18447       1656 /tmp/test1
    [sergej@surg-adm ~]$ lsof | grep /tmp/test1
    ping      301543                           sergej    1w      REG               0,35     24423       1656 /tmp/test1 (deleted)
    [sergej@surg-adm ~]$ cat /proc/301543/fd/1 > /tmp/test1
    [sergej@surg-adm ~]$ cat /tmp/test1
    PING ya.ru (87.250.250.242) 56(84) bytes of data.
    64 bytes from ya.ru (87.250.250.242): icmp_seq=1 ttl=249 time=49.3 ms
    64 bytes from ya.ru (87.250.250.242): icmp_seq=2 ttl=249 time=49.1 ms
    64 bytes from ya.ru (87.250.250.242): icmp_seq=3 ttl=249 time=49.0 ms
    64 bytes from ya.ru (87.250.250.242): icmp_seq=4 ttl=249 time=48.9 ms
    64 bytes from ya.ru (87.250.250.242): icmp_seq=5 ttl=249 time=49.0 ms
    64 bytes from ya.ru (87.250.250.242): icmp_seq=6 ttl=249 time=48.9 ms
    64 bytes from ya.ru (87.250.250.242): icmp_seq=7 ttl=249 time=48.9 ms
    64 bytes from ya.ru (87.250.250.242): icmp_seq=8 ttl=249 time=49.2 ms
    64 bytes from ya.ru (87.250.250.242): icmp_seq=9 ttl=249 time=49.1 ms
    ...
    [sergej@surg-adm ~]$ ls -l /tmp
    итого 100
    -rw-r--r-- 1 sergej sergej    94 янв 18 12:34 847bf70473fa93942054bb1d51dd24d6-{87A94AB0-E370-4cde-98D3-ACC110C5967D
    -rw-rw-r-- 1 sergej sergej 35511 янв 19 10:47 test1
```

    _Пояснения_
    в первом выводе видем запущеный процес пинга в файл что он работает
    во втором выводе видем что процес работает, а сам файл удален
    и далие из процесса делаем запись в файл и выводим файл.
    
    ### Как то так

```shell
    [sergej@surg-adm ~]$ ls -l /tmp
    итого 4
    -rw-r--r-- 1 root root   0 янв 13 21:43 log
    drwx------ 3 root root  16 дек 31 19:40 systemd-private-8eb22daf2c6b4b308cd9b3f9b6bf85c5-chronyd.service-hTDJh9
    drwx------ 3 root root  16 дек 31 19:40 systemd-private-8eb22daf2c6b4b308cd9b3f9b6bf85c5-httpd.service-FsXhDL
    drwx------ 3 root root  16 дек 31 19:40 systemd-private-8eb22daf2c6b4b308cd9b3f9b6bf85c5-openvpn@server.service-fd67Qz
    drwx------ 3 root root  16 дек 31 19:40 systemd-private-8eb22daf2c6b4b308cd9b3f9b6bf85c5-tor.service-7Vybwa
    -rw-r--r-- 1 root root 407 янв 20 20:12 test1
    [sergej@surg-adm ~]$ cat /tmp/test1
    PING ya.ru (87.250.250.242) 56(84) bytes of data.
    64 bytes from ya.ru (87.250.250.242): icmp_seq=1 ttl=248 time=56.5 ms
    64 bytes from ya.ru (87.250.250.242): icmp_seq=2 ttl=248 time=55.0 ms
    64 bytes from ya.ru (87.250.250.242): icmp_seq=3 ttl=248 time=57.3 ms
    
    [sergej@surg-adm ~]$ lsof | grep /tmp/test1
    ping      301543                           sergej    1w      REG               0,35     18447       1656 /tmp/test1
    [sergej@surg-adm ~]$ rm /tmp/test1
    rm: удалить обычный файл «/tmp/test1»? yes
    [sergej@surg-adm ~]$ ls -l /tmp
    итого 0
    -rw-r--r-- 1 root root  0 янв 13 21:43 log
    drwx------ 3 root root 16 дек 31 19:40 systemd-private-8eb22daf2c6b4b308cd9b3f9b6bf85c5-chronyd.service-hTDJh9
    drwx------ 3 root root 16 дек 31 19:40 systemd-private-8eb22daf2c6b4b308cd9b3f9b6bf85c5-httpd.service-FsXhDL
    drwx------ 3 root root 16 дек 31 19:40 systemd-private-8eb22daf2c6b4b308cd9b3f9b6bf85c5-openvpn@server.service-fd67Qz
    drwx------ 3 root root 16 дек 31 19:40 systemd-private-8eb22daf2c6b4b308cd9b3f9b6bf85c5-tor.service-7Vybwa
    [sergej@surg-adm ~]$ cat /tmp/test1
    cat: /tmp/test1: Нет такого файла или каталога
    [sergej@surg-adm ~]$ lsof | grep /tmp/test1
    ping      301543                           sergej    1w      REG               0,35     24423       1656 /tmp/test1 (deleted)
    
    ## [sergej@surg-adm ~]$  echo ' ' > /proc/301543/fd/1
```

### 4. Занимают ли зомби-процессы какие-то ресурсы в ОС (CPU, RAM, IO)?

    "Зомби" процессы, в отличии от "сирот" освобождают свои ресурсы, но не освобождают запись в таблице процессов. Запись освободиться при вызове wait() родительским процессом.

### 5. В iovisor BCC есть утилита opensnoop

```shell
    root@vagrant:~# dpkg -L bpfcc-tools | grep sbin/opensnoop
    /usr/sbin/opensnoop-bpfcc
```

На какие файлы вы увидели вызовы группы open за первую секунду работы утилиты? Воспользуйтесь пакетом bpfcc-tools для Ubuntu 20.04. Дополнительные сведения по установке.

```shell
    [sergej@surg-adm tools]$ sudo dnf install bcc
    [sergej@surg-adm ~]$ cd /usr/share/bcc/tools
    [sergej@surg-adm tools]$ sudo ./opensnoop
    [sudo] пароль для sergej: 
    PID    COMM               FD ERR PATH
    889    systemd-oomd        6   0 /proc/meminfo
    2392   Viber              86   0 /usr/share/zoneinfo/Asia/Yekaterinburg
    2392   Viber              86   0 /usr/share/zoneinfo/Asia/Yekaterinburg
    2392   Viber              86   0 /usr/share/zoneinfo/Asia/Yekaterinburg
    2392   Viber              86   0 /usr/share/zoneinfo/Asia/Yekaterinburg
    889    systemd-oomd        6   0 /proc/meminfo
    934    in:imjournal       29   0 /var/log/journal/8c20bed4bb5c404a94103f87f30bccc5/system.journal
    1221   abrt-dump-journ     6   0 /var/log/journal/8c20bed4bb5c404a94103f87f30bccc5/system.journal
    1220   abrt-dump-journ     6   0 /var/log/journal/8c20bed4bb5c404a94103f87f30bccc5/system.journal
    1236   abrt-dump-journ     6   0 /var/log/journal/8c20bed4bb5c404a94103f87f30bccc5/system.journal
    7091   gnome-terminal-    14   0 /tmp
```

### 6. Какой системный вызов использует uname -a? Приведите цитату из man по этому системному вызову, где описывается альтернативное местоположение в /proc, где можно узнать версию ядра и релиз ОС

системный вызов uname()
    Цитата :
    > Part of the utsname information is also accessible  via  /proc/sys/kernel/{ostype, hostname, osrelease, version, domainname}.
    > cat /etc/redhat-release выводит версию и релиз

### 7. Чем отличается последовательность команд через ; и через && в bash? Например

```shell
    root@netology1:~# test -d /tmp/some_dir; echo Hi
    Hi
    root@netology1:~# test -d /tmp/some_dir && echo Hi
    root@netology1:~#
```

    Есть ли смысл использовать в bash &&, если применить set -e?
    
    && -  условный оператор, 
    ;  - разделитель последовательных команд

    test -d /tmp/some_dir && echo Hi - в данном случае echo  отработает только при успешном заверщении команды test

    set -e - прерывает сессию при любом ненулевом значении исполняемых команд в конвеере кроме последней. В случае &&  вместе с set -e- вероятно не имеет смысла, так как при ошибке, выполнение команд прекратиться.

### 8. Из каких опций состоит режим bash set -euxo pipefail и почему его хорошо было бы использовать в сценариях?

    -e прерывает выполнение исполнения при ошибке любой команды кроме последней в последовательности 
    -x вывод трейса простых команд 
    -u неустановленные/не заданные параметры и переменные считаются как ошибки, с выводом в stderr текста ошибки и выполнит завершение неинтерактивного вызова
    -o pipefail возвращает код возврата набора/последовательности команд, ненулевой при последней команды или 0 для успешного выполнения команд.

    Повышает деталезацию вывода ошибок(логирования), и завершит сценарий при наличии ошибок, на любом этапе выполнения сценария, кроме последней завершающей команды.

### 9. Используя -o stat для ps, определите, какой наиболее часто встречающийся статус у процессов в системе. В man ps ознакомьтесь (/PROCESS STATE CODES) что значат дополнительные к основной заглавной буквы статуса процессов. Его можно не учитывать при расчете (считать S, Ss или Ssl равнозначными)

    Самый часто встречающийся статус это - S

   PROCESS STATE CODES

       Here are the different values that the s, stat and state output specifiers (header "STAT" or "S") will display to describe the state of a process:
       D    uninterruptible sleep (usually IO)
       R    running or runnable (on run queue)
       S    interruptible sleep (waiting for an event to complete)
       T    stopped, either by a job control signal or because it is being traced.
       W    paging (not valid since the 2.6.xx kernel)
       X    dead (should never be seen)
       Z    defunct ("zombie") process, terminated but not reaped by its parent.

       For BSD formats and when the stat keyword is used, additional characters may be displayed:
       <    high-priority (not nice to other users)
       N    low-priority (nice to other users)
       L    has pages locked into memory (for real-time and custom IO)
       s    is a session leader
       l    is multi-threaded (using CLONE_THREAD, like NPTL pthreads do)
       +    is in the foreground process group.
