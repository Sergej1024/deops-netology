## Домашнее задание к занятию "3.4. Операционные системы, лекция 2"

### 1. На лекции мы познакомились с node_exporter. В демонстрации его исполняемый файл запускался в background. Этого достаточно для демо, но не для настоящей production-системы, где процессы должны находиться под внешним управлением. Используя знания из лекции по systemd, создайте самостоятельно простой unit-файл для node_exporter

    • поместите его в автозагрузку, 
    • предусмотрите возможность добавления опций к запускаемому процессу через внешний файл (посмотрите, например, на systemctl cat cron), 
    • удостоверьтесь, что с помощью systemctl процесс корректно стартует, завершается, а после перезагрузки автоматически поднимается. 

```shell
[root@centos8 vagrant]# useradd -M -r -s /bin/false node_exporter
[root@centos8 vagrant]# id node_exporter
uid=993(node_exporter) gid=990(node_exporter) groups=990(node_exporter)
[root@centos8 vagrant]# wget https://github.com/prometheus/node_exporter/releases/download/v1.3.1/node_exporter-1.3.1.linux-amd64.tar.gz -P /tmp
[root@centos8 vagrant]# cd /tmp
[root@centos8 tmp]# tar xzf node_exporter-1.3.1.linux-amd64.tar.gz
[root@centos8 tmp]# cp node_exporter-1.3.1.linux-amd64/node_exporter /opt
[root@centos8 tmp]# chown node_exporter:node_exporter /opt/node_exporter
[root@centos8 tmp]# mcedit /etc/systemd/system/node_exporter@.service
[root@centos8 tmp]# systemctl daemon-reload
[root@centos8 tmp]# systemctl enable node_exporter.service
Created symlink /etc/systemd/system/multi-user.target.wants/node_exporter.service → /etc/systemd/system/node_exporter.service.
[root@centos8 tmp]# systemctl start node_exporter.service
[root@centos8 tmp]# firewall-cmd --zone=public --add-port=9100/tcp --permanent
[root@centos8 tmp]# cat /etc/systemd/system/node_exporter@.service
[Unit]
Description=Prometheus Node Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/opt/node_exporter -C /etc/default/node_exporter/%i.conf

[Install]
WantedBy=multi-user.target
```

> Запуск с доп. параметрами производится systemctl enable node_exporter@configsetting.service

### 2.Ознакомьтесь с опциями node_exporter и выводом /metrics по-умолчанию. Приведите несколько опций, которые вы бы выбрали для базового мониторинга хоста по CPU, памяти, диску и сети

CPU:

    node_cpu_seconds_total{cpu="0",mode="idle"} 1131.7
    node_cpu_seconds_total{cpu="0",mode="system"} 3.5
    node_cpu_seconds_total{cpu="0",mode="user"} 3.6
    process_cpu_seconds_total

Memory:

    node_memory_MemAvailable_bytes 
    node_memory_MemFree_bytes

Disk(если несколько дисков то для каждого):

    node_disk_io_time_seconds_total{device="sda"} 
    node_disk_read_bytes_total{device="sda"} 
    node_disk_read_time_seconds_total{device="sda"} 
    node_disk_write_time_seconds_total{device="sda"}

Network(так же для каждого активного адаптера):

    node_network_receive_errs_total{device="eth0"} 
    node_network_receive_bytes_total{device="eth0"} 
    node_network_transmit_bytes_total{device="eth0"}
    node_network_transmit_errs_total{device="eth0"}

### 3.Установите в свою виртуальную машину Netdata. Воспользуйтесь готовыми пакетами для установки (sudo apt install -y netdata). После успешной установки

    • в конфигурационном файле /etc/netdata/netdata.conf в секции [web] замените значение с localhost на bind to = 0.0.0.0, 
    • добавьте в Vagrantfile проброс порта Netdata на свой локальный компьютер и сделайте vagrant reload: 
config.vm.network "forwarded_port", guest: 19999, host: 19999
После успешной перезагрузки в браузере на своем ПК (не в виртуальной машине) вы должны суметь зайти на localhost:19999. Ознакомьтесь с метриками, которые по умолчанию собираются Netdata и с комментариями, которые даны к этим метрикам.

```shell
[root@centos8 vagrant]# dnf install netdata
[root@centos8 vagrant]# firewall-cmd --zone=public --add-port=19999/tcp --permanent

[root@centos8 vagrant]# systemctl start netdata
[root@centos8 vagrant]# ss -altnp | grep 19
LISTEN 0      128          0.0.0.0:19999      0.0.0.0:*    users:(("netdata",pid=1873,fd=5))
[root@centos8 vagrant]# systemctl enable netdata
Created symlink /etc/systemd/system/multi-user.target.wants/netdata.service → /usr/lib/systemd/system/netdata.service.
```

### 4.Можно ли по выводу dmesg понять, осознает ли ОС, что загружена не на настоящем оборудовании, а на системе виртуализации?

```shell
[vagrant@centos8 ~]$ dmesg | grep virtualiz
[    0.000000] CPU MTRRs all blank - virtualized system.
[    0.000000] Booting paravirtualized kernel on KVM
[    1.013167] systemd[1]: Detected virtualization oracle.
[    2.590498] systemd[1]: Detected virtualization oracle.
```

### 5.Как настроен sysctl fs.nr_open на системе по-умолчанию? Узнайте, что означает этот параметр. Какой другой существующий лимит не позволит достичь такого числа (ulimit --help)?

```shell
[root@centos8 vagrant]#  /sbin/sysctl -n fs.nr_open
1048576
```

Это максимальное число открытых дескрипторов для ядра (системы), для пользователя задать больше этого числа нельзя (если не менять).
Число задается кратное 1024, в данном случае =1024*1024.

Но макс.предел ОС можно посмотреть так:

```shell
[root@centos8 vagrant]# cat /proc/sys/fs/file-max
181626
```

```sh
[root@centos8 vagrant]# ulimit -Sn
1024
```

мягкий лимит (так же ulimit –n) на пользователя (может быть увеличен процессом в процессе работы)

```shell
[root@centos8 vagrant]# ulimit -Hn
262144
```

жесткий лимит на пользователя (не может быть увеличен, только уменьшен)

Оба ulimit -n НЕ могут превысить системный fs.nr_open

### 6.Запустите любой долгоживущий процесс (не ls, который отработает мгновенно, а, например, sleep 1h) в отдельном неймспейсе процессов; покажите, что ваш процесс работает под PID 1 через nsenter. Для простоты работайте в данном задании под root (sudo -i). Под обычным пользователем требуются дополнительные опции (--map-root-user) и т.д

```shell
[root@centos8 vagrant]# screen
[root@centos8 vagrant]# unshare -f --pid --mount-proc /bin/bash
[root@centos8 vagrant]# ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.1  0.2  27144  4772 pts/1    S    16:43   0:00 /bin/bash
root          18  0.0  0.2  58736  3908 pts/1    R+   16:43   0:00 ps aux
```

### 7.Найдите информацию о том, что такое :(){ :|:& };:. Запустите эту команду в своей виртуальной машине Vagrant с Ubuntu 20.04 (это важно, поведение в других ОС не проверялось). Некоторое время все будет "плохо", после чего (минуты) – ОС должна стабилизироваться. Вызов dmesg расскажет, какой механизм помог автоматической стабилизации. Как настроен этот механизм по-умолчанию, и как изменить число процессов, которое можно создать в сессии?

Из предыдущих лекций ясно что это функция внутри "{}", судя по всему с именем ":" , которая после определения в строке запускает саму себя.
внутренности через поиск нагуглил, порождает два фоновых процесса самой себя,
получается этакое бинарное дерево, плодящее процессы

А функционал судя по всему этот:

```shell
[ 1222.124110] cgroup: fork rejected by pids controller in /user.slice/user-1000.slice/session-3.scope
```

Судя по всему, система на основании этих файлов в пользовательской зоне ресурсов имеет определенное ограничение на создаваемые ресурсы
и соответственно при превышении начинает блокировать создание числа

Если установить ulimit -u 50 - число процессов будет ограниченно 50 для пользователя.
