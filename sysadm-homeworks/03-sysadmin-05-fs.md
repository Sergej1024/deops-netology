## Домашнее задание к занятию "3.5. Файловые системы"

### 1. Узнайте о sparse (разряженных) файлах

Хороший способ уменьшения места на диске и увеличения производительности чтения.

### 2. Могут ли файлы, являющиеся жесткой ссылкой на один объект, иметь разные права доступа и владельца? Почему?

Так как hardlink это ссылка на тот же самый файл и имеет тот же inode то права и владелец будут одни и теже.

### 3. Сделайте vagrant destroy на имеющийся инстанс Ubuntu. Замените содержимое Vagrantfile следующим

```shell
    Vagrant.configure("2") do |config|
      config.vm.box = "bento/ubuntu-20.04"
      config.vm.provider :virtualbox do |vb|
        lvm_experiments_disk0_path = "/tmp/lvm_experiments_disk0.vmdk"
        lvm_experiments_disk1_path = "/tmp/lvm_experiments_disk1.vmdk"
        vb.customize ['createmedium', '--filename', lvm_experiments_disk0_path, '--size', 2560]
        vb.customize ['createmedium', '--filename', lvm_experiments_disk1_path, '--size', 2560]
        vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 1, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk0_path]
        vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 2, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk1_path]
      end
    end
```

Данная конфигурация создаст новую виртуальную машину с двумя дополнительными неразмеченными дисками по 2.5 Гб.

```shell
vagrant@vagrant:~$ lsblk
NAME                      MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
loop0                       7:0    0 70.3M  1 loop /snap/lxd/21029
loop1                       7:1    0 32.3M  1 loop /snap/snapd/12704
loop2                       7:2    0 55.4M  1 loop /snap/core18/2128
loop3                       7:3    0 43.4M  1 loop /snap/snapd/14549
loop4                       7:4    0 55.5M  1 loop /snap/core18/2284
loop5                       7:5    0 61.9M  1 loop /snap/core20/1270
loop6                       7:6    0 67.2M  1 loop /snap/lxd/21835
sda                         8:0    0   64G  0 disk 
├─sda1                      8:1    0    1M  0 part 
├─sda2                      8:2    0    1G  0 part /boot
└─sda3                      8:3    0   63G  0 part 
  └─ubuntu--vg-ubuntu--lv 253:0    0 31.5G  0 lvm  /
sdb                         8:16   0  2.5G  0 disk 
sdc                         8:32   0  2.5G  0 disk 
```

### 4. Используя fdisk, разбейте первый диск на 2 раздела: 2 Гб, оставшееся пространство

```shell
vagrant@vagrant:~$ sudo -i
root@vagrant:~# fdisk /dev/sdb

Welcome to fdisk (util-linux 2.34).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Device does not contain a recognized partition table.
Created a new DOS disklabel with disk identifier 0x5604b4ec.

Command (m for help): n
Partition type
   p   primary (0 primary, 0 extended, 4 free)
   e   extended (container for logical partitions)
Select (default p): p
Partition number (1-4, default 1): 1
First sector (2048-5242879, default 2048): 
Last sector, +/-sectors or +/-size{K,M,G,T,P} (2048-5242879, default 5242879): +2G

Created a new partition 1 of type 'Linux' and of size 2 GiB.

Command (m for help): w
The partition table has been altered.
Calling ioctl() to re-read partition table.
Syncing disks.

root@vagrant:~# fdisk /dev/sdb

Welcome to fdisk (util-linux 2.34).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.


Command (m for help): n
Partition type
   p   primary (1 primary, 0 extended, 3 free)
   e   extended (container for logical partitions)
Select (default p): p
Partition number (2-4, default 2): 2
First sector (4196352-5242879, default 4196352): 
Last sector, +/-sectors or +/-size{K,M,G,T,P} (4196352-5242879, default 5242879): 

Created a new partition 2 of type 'Linux' and of size 511 MiB.

Command (m for help): w
The partition table has been altered.
Calling ioctl() to re-read partition table.
Syncing disks.

root@vagrant:~# fdisk -l /dev/sdb
Disk /dev/sdb: 2.51 GiB, 2684354560 bytes, 5242880 sectors
Disk model: VBOX HARDDISK   
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x5604b4ec

Device     Boot   Start     End Sectors  Size Id Type
/dev/sdb1          2048 4196351 4194304    2G 83 Linux
/dev/sdb2       4196352 5242879 1046528  511M 83 Linux
```

### 5. Используя sfdisk, перенесите данную таблицу разделов на второй диск

```shell
root@vagrant:~# sfdisk -d /dev/sdb|sfdisk --force /dev/sdc
Checking that no-one is using this disk right now ... OK

Disk /dev/sdc: 2.51 GiB, 2684354560 bytes, 5242880 sectors
Disk model: VBOX HARDDISK   
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x06b31b40

Old situation:

>>> Script header accepted.
>>> Script header accepted.
>>> Script header accepted.
>>> Script header accepted.
>>> Created a new DOS disklabel with disk identifier 0x5604b4ec.
/dev/sdc1: Created a new partition 1 of type 'Linux' and of size 2 GiB.
/dev/sdc2: Created a new partition 2 of type 'Linux' and of size 511 MiB.
/dev/sdc3: Done.

New situation:
Disklabel type: dos
Disk identifier: 0x5604b4ec

Device     Boot   Start     End Sectors  Size Id Type
/dev/sdc1          2048 4196351 4194304    2G 83 Linux
/dev/sdc2       4196352 5242879 1046528  511M 83 Linux

The partition table has been altered.
Calling ioctl() to re-read partition table.
Syncing disks.
oot@vagrant:~# fdisk -l /dev/sdc
Disk /dev/sdc: 2.51 GiB, 2684354560 bytes, 5242880 sectors
Disk model: VBOX HARDDISK   
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x5604b4ec

Device     Boot   Start     End Sectors  Size Id Type
/dev/sdc1          2048 4196351 4194304    2G 83 Linux
/dev/sdc2       4196352 5242879 1046528  511M 83 Linux

```

### 6. Соберите mdadm RAID1 на паре разделов 2 Гб

```shell
root@vagrant:~# mdadm --create --verbose /dev/md1 -l 1 -n 2 /dev/sd{b1,c1}
mdadm: Note: this array has metadata at the start and
    may not be suitable as a boot device.  If you plan to
    store '/boot' on this device please ensure that
    your boot-loader understands md/v1.x metadata, or use
    --metadata=0.90
mdadm: size set to 2094080K
Continue creating array? y
mdadm: Defaulting to version 1.2 metadata
mdadm: array /dev/md1 started.
root@vagrant:~# 
```

### 7. Соберите mdadm RAID0 на второй паре маленьких разделов

```shell
root@vagrant:~# mdadm --create --verbose /dev/md0 -l 1 -n 2 /dev/sd{b2,c2}
mdadm: Note: this array has metadata at the start and
    may not be suitable as a boot device.  If you plan to
    store '/boot' on this device please ensure that
    your boot-loader understands md/v1.x metadata, or use
    --metadata=0.90
mdadm: size set to 522240K
Continue creating array? y
mdadm: Defaulting to version 1.2 metadata
mdadm: array /dev/md0 started.

```

### 8. Создайте 2 независимых PV на получившихся md-устройствах

```shell
root@vagrant:~# pvcreate /dev/md1 /dev/md0
  Physical volume "/dev/md1" successfully created.
  Physical volume "/dev/md0" successfully created.
root@vagrant:~# pvdisplay
  --- Physical volume ---
  PV Name               /dev/sda3
  VG Name               ubuntu-vg
  PV Size               <63.00 GiB / not usable 0   
  Allocatable           yes 
  PE Size               4.00 MiB
  Total PE              16127
  Free PE               8063
  Allocated PE          8064
  PV UUID               sDUvKe-EtCc-gKuY-ZXTD-1B1d-eh9Q-XldxLf
   
  --- Physical volume ---
  PV Name               /dev/md1
  VG Name               vg1
  PV Size               <2.00 GiB / not usable 0   
  Allocatable           yes 
  PE Size               4.00 MiB
  Total PE              511
  Free PE               511
  Allocated PE          0
  PV UUID               naL5Ag-1ZCL-CgxF-OGvo-ZDdo-OL0U-zwsUV8
   
  --- Physical volume ---
  PV Name               /dev/md0
  VG Name               vg1
  PV Size               510.00 MiB / not usable 2.00 MiB
  Allocatable           yes 
  PE Size               4.00 MiB
  Total PE              127
  Free PE               127
  Allocated PE          0
  PV UUID               MIfsuI-fSHQ-Y8Nn-fbNi-zPyb-W3Ra-g2iBRU

```

### 9. Создайте общую volume-group на этих двух PV

```shell
root@vagrant:~# vgcreate vg1 /dev/md1 /dev/md0
  Volume group "vg1" successfully created
root@vagrant:~# vgdisplay
  --- Volume group ---
  VG Name               ubuntu-vg
  System ID             
  Format                lvm2
  Metadata Areas        1
  Metadata Sequence No  2
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                1
  Open LV               1
  Max PV                0
  Cur PV                1
  Act PV                1
  VG Size               <63.00 GiB
  PE Size               4.00 MiB
  Total PE              16127
  Alloc PE / Size       8064 / 31.50 GiB
  Free  PE / Size       8063 / <31.50 GiB
  VG UUID               aK7Bd1-JPle-i0h7-5jJa-M60v-WwMk-PFByJ7
   
  --- Volume group ---
  VG Name               vg1
  System ID             
  Format                lvm2
  Metadata Areas        2
  Metadata Sequence No  1
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                0
  Open LV               0
  Max PV                0
  Cur PV                2
  Act PV                2
  VG Size               2.49 GiB
  PE Size               4.00 MiB
  Total PE              638
  Alloc PE / Size       0 / 0   
  Free  PE / Size       638 / 2.49 GiB
  VG UUID               QVbIHH-4N7a-q3oy-n8kf-1J6b-wFa0-X8Ir3Z

```

### 10. Создайте LV размером 100 Мб, указав его расположение на PV с RAID0

```shell
root@vagrant:~# lvcreate -L 100M vg1 /dev/md0
  Logical volume "lvol0" created.
root@vagrant:~# vgs
  VG        #PV #LV #SN Attr   VSize   VFree  
  ubuntu-vg   1   1   0 wz--n- <63.00g <31.50g
  vg1         2   1   0 wz--n-   2.49g   2.39g
root@vagrant:~# lvs
  LV        VG        Attr       LSize   Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
  ubuntu-lv ubuntu-vg -wi-ao----  31.50g                                                    
  lvol0     vg1       -wi-a----- 100.00m 
```

### 11. Создайте mkfs.ext4 ФС на получившемся LV

```shell
root@vagrant:~# mkfs.ext4 /dev/vg1/lvol0
mke2fs 1.45.5 (07-Jan-2020)
Creating filesystem with 25600 4k blocks and 25600 inodes

Allocating group tables: done                            
Writing inode tables: done                            
Creating journal (1024 blocks): done
Writing superblocks and filesystem accounting information: done

```

### 12. Смонтируйте этот раздел в любую директорию, например, /tmp/new

```shell
root@vagrant:~# mkdir /tmp/new
root@vagrant:~# mount /dev/vg1/lvol0 /tmp/new
root@vagrant:~# df -h
Filesystem                         Size  Used Avail Use% Mounted on
udev                               447M     0  447M   0% /dev
tmpfs                               99M 1016K   98M   2% /run
/dev/mapper/ubuntu--vg-ubuntu--lv   31G  3.7G   26G  13% /
tmpfs                              491M     0  491M   0% /dev/shm
tmpfs                              5.0M     0  5.0M   0% /run/lock
tmpfs                              491M     0  491M   0% /sys/fs/cgroup
/dev/loop0                          71M   71M     0 100% /snap/lxd/21029
/dev/sda2                          976M  107M  803M  12% /boot
/dev/loop1                          33M   33M     0 100% /snap/snapd/12704
/dev/loop2                          56M   56M     0 100% /snap/core18/2128
vagrant                            362G   93G  270G  26% /vagrant
/dev/loop3                          44M   44M     0 100% /snap/snapd/14549
/dev/loop4                          56M   56M     0 100% /snap/core18/2284
tmpfs                               99M     0   99M   0% /run/user/1000
/dev/loop5                          62M   62M     0 100% /snap/core20/1270
/dev/loop6                          68M   68M     0 100% /snap/lxd/21835
/dev/mapper/vg1-lvol0               93M   72K   86M   1% /tmp/new

```

### 13. Поместите туда тестовый файл, например wget <https://mirror.yandex.ru/ubuntu/ls-lR.gz> -O /tmp/new/test.gz

```shell
root@vagrant:~# wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz
--2022-01-26 06:12:22--  https://mirror.yandex.ru/ubuntu/ls-lR.gz
Resolving mirror.yandex.ru (mirror.yandex.ru)... 213.180.204.183, 2a02:6b8::183
Connecting to mirror.yandex.ru (mirror.yandex.ru)|213.180.204.183|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 22043739 (21M) [application/octet-stream]
Saving to: ‘/tmp/new/test.gz’

/tmp/new/test.gz                                            100%[==================>]  21.02M  10.5MB/s    in 2.0s    

2022-01-26 06:12:24 (10.5 MB/s) - ‘/tmp/new/test.gz’ saved [22043739/22043739]

root@vagrant:~# ls -l /tmp/new
total 21544
drwx------ 2 root root    16384 Jan 26 06:10 lost+found
-rw-r--r-- 1 root root 22043739 Jan 26 01:25 test.gz

```

### 14. Прикрепите вывод lsblk

```shell
root@vagrant:~# lsblk
NAME                      MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
loop0                       7:0    0 70.3M  1 loop  /snap/lxd/21029
loop1                       7:1    0 32.3M  1 loop  /snap/snapd/12704
loop2                       7:2    0 55.4M  1 loop  /snap/core18/2128
loop3                       7:3    0 43.4M  1 loop  /snap/snapd/14549
loop4                       7:4    0 55.5M  1 loop  /snap/core18/2284
loop5                       7:5    0 61.9M  1 loop  /snap/core20/1270
loop6                       7:6    0 67.2M  1 loop  /snap/lxd/21835
sda                         8:0    0   64G  0 disk  
├─sda1                      8:1    0    1M  0 part  
├─sda2                      8:2    0    1G  0 part  /boot
└─sda3                      8:3    0   63G  0 part  
  └─ubuntu--vg-ubuntu--lv 253:0    0 31.5G  0 lvm   /
sdb                         8:16   0  2.5G  0 disk  
├─sdb1                      8:17   0    2G  0 part  
│ └─md1                     9:1    0    2G  0 raid1 
└─sdb2                      8:18   0  511M  0 part  
  └─md0                     9:0    0  510M  0 raid1 
    └─vg1-lvol0           253:1    0  100M  0 lvm   /tmp/new
sdc                         8:32   0  2.5G  0 disk  
├─sdc1                      8:33   0    2G  0 part  
│ └─md1                     9:1    0    2G  0 raid1 
└─sdc2                      8:34   0  511M  0 part  
  └─md0                     9:0    0  510M  0 raid1 
    └─vg1-lvol0           253:1    0  100M  0 lvm   /tmp/new

```

### 15. Протестируйте целостность файла

```shell
    root@vagrant:~# gzip -t /tmp/new/test.gz
    root@vagrant:~# echo $?
    0
```

```shell
root@vagrant:~# gzip -t /tmp/new/test.gz && echo $?
0
```

### 16. Используя pvmove, переместите содержимое PV с RAID0 на RAID1

```shell
root@vagrant:~# pvmove /dev/md0
  /dev/md0: Moved: 12.00%
  /dev/md0: Moved: 100.00%
root@vagrant:~# lsblk
NAME                      MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
loop0                       7:0    0 70.3M  1 loop  /snap/lxd/21029
loop1                       7:1    0 32.3M  1 loop  /snap/snapd/12704
loop2                       7:2    0 55.4M  1 loop  /snap/core18/2128
loop3                       7:3    0 43.4M  1 loop  /snap/snapd/14549
loop4                       7:4    0 55.5M  1 loop  /snap/core18/2284
loop5                       7:5    0 61.9M  1 loop  /snap/core20/1270
loop6                       7:6    0 67.2M  1 loop  /snap/lxd/21835
sda                         8:0    0   64G  0 disk  
├─sda1                      8:1    0    1M  0 part  
├─sda2                      8:2    0    1G  0 part  /boot
└─sda3                      8:3    0   63G  0 part  
  └─ubuntu--vg-ubuntu--lv 253:0    0 31.5G  0 lvm   /
sdb                         8:16   0  2.5G  0 disk  
├─sdb1                      8:17   0    2G  0 part  
│ └─md1                     9:1    0    2G  0 raid1 
│   └─vg1-lvol0           253:1    0  100M  0 lvm   /tmp/new
└─sdb2                      8:18   0  511M  0 part  
  └─md0                     9:0    0  510M  0 raid1 
sdc                         8:32   0  2.5G  0 disk  
├─sdc1                      8:33   0    2G  0 part  
│ └─md1                     9:1    0    2G  0 raid1 
│   └─vg1-lvol0           253:1    0  100M  0 lvm   /tmp/new
└─sdc2                      8:34   0  511M  0 part  
  └─md0                     9:0    0  510M  0 raid1 
```

### 17. Сделайте --fail на устройство в вашем RAID1 md

```shell
root@vagrant:~# mdadm /dev/md1 --fail /dev/sdb1
mdadm: set /dev/sdb1 faulty in /dev/md1
```

### 18. Подтвердите выводом dmesg, что RAID1 работает в деградированном состоянии

```shell
root@vagrant:~# dmesg |grep md1
[ 9631.073468] md/raid1:md1: not clean -- starting background reconstruction
[ 9631.073473] md/raid1:md1: active with 2 out of 2 mirrors
[ 9631.073516] md1: detected capacity change from 0 to 2144337920
[ 9631.076541] md: resync of RAID array md1
[ 9641.304226] md: md1: resync done.
[10638.428156] md/raid1:md1: Disk failure on sdb1, disabling device.
               md/raid1:md1: Operation continuing on 1 devices.
```

### 19. Протестируйте целостность файла, несмотря на "сбойный" диск он должен продолжать быть доступен

```shell
    root@vagrant:~# gzip -t /tmp/new/test.gz
    root@vagrant:~# echo $?
    0
```

```shell
root@vagrant:~# gzip -t /tmp/new/test.gz && echo $?
0
```

### 20. Погасите тестовый хост, vagrant destroy

```shell
root@surg-adm sergej]# vagrant destroy
    default: Are you sure you want to destroy the 'default' VM? [y/N] y
==> default: Forcing shutdown of VM...
==> default: Destroying VM and associated drives...
```
