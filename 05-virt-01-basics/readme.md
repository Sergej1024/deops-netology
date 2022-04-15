## Домашнее задание к занятию "5.1. Введение в виртуализацию. Типы и функции гипервизоров. Обзор рынка вендоров и областей применения."

### Задача 1

Опишите кратко, как вы поняли: в чем основное отличие полной (аппаратной) виртуализации, паравиртуализации и виртуализации на основе ОС.

- Аппаратная виртуализация это по сути установленный гипервизор на железо выполняющий для этого железа функцию ОС.
- Паравиртуализация это приложение устанавливаемое на ОС и разделяющее процесс с гостевой ОС, позволяет запускать гостевые ОС отличные от хостовой.
- Виртуализация на основе ОС запускает изолированные виртуальные машиины, но не позволяет запускать ОС с отличающимся ядром от хостовой машины.

### Задача 2

Выберите один из вариантов использования организации физических серверов, в зависимости от условий использования.

Организация серверов:
- физические сервера, 
- паравиртуализация, 
- виртуализация уровня ОС.

Условия использования:
- Высоконагруженная база данных, чувствительная к отказу.
- Различные web-приложения. 
- Windows системы для использования бухгалтерским отделом. 
- Системы, выполняющие высокопроизводительные расчеты на GPU.

Опишите, почему вы выбрали к каждому целевому использованию такую организацию.

Высоконагруженная база данных, чувствительная к отказу:

    Базы данных в принципе хранятся на СХД физически и подключаются к ОС по ISCSI, в таком виде не важно к виртуальной машине или физическому серверу подключена луна.
    Но в случае когда нет средств на СХД, но есть физический сервер то лучше использовать его, нет гипервизора седающего часть ресурсов.

Различные web-приложения:

    виртуализация уровня ОС - выше скоросто масштабирования при необходимости расширения, нет жестких требований к аппаратным ресурсам

Windows системы для использования бухгалтерским отделом:

    паравиртуализация -легко расширяемая по ресурсам за счет гипервизора, удобство миграции, удобное создание бекапов и их восстановление на любой доступный гипервизор.

Системы, выполняющие высокопроизводительные расчеты на GPU:

    физические сервера - возможность задействовать все ресурсы доступные изхостовой ОС.

### Задача 3

Выберите подходящую систему управления виртуализацией для предложенного сценария. Детально опишите ваш выбор.

Сценарии:
- 100 виртуальных машин на базе Linux и Windows, общие задачи, нет особых требований. Преимущественно Windows based инфраструктура, требуется реализация программных балансировщиков нагрузки, репликации данных и автоматизированного механизма создания резервных копий. 
- Требуется наиболее производительное бесплатное open source решение для виртуализации небольшой (20-30 серверов) инфраструктуры на базе Linux и Windows виртуальных машин. 
- Необходимо бесплатное, максимально совместимое и производительное решение для виртуализации Windows инфраструктуры. 
- Необходимо рабочее окружение для тестирования программного продукта на нескольких дистрибутивах Linux.

1. Я бы выбрал ESXI (в принципе так и выбрано в организации) он бесплатный, особого обучения не требует (самостоятельно разобрался за пару дней), есть удобное средство миграции с одного гипервизора на другой бесплатное.
2. Опят таки я бы выбрал KVM возможно с надстройкой ovirt для удобства обслуживания. На лекции больше склоняли к XEN, про него ничего не могу сказать не сталкивался
3. Из лекции ответ Hyper-V, но я бы не стал им пользоваться, плохие воспоминания, возможно из-за неопытности. А так лучше бы выбрал ESXI, тоже бесплатный и на мой взгляд работает стабилние.
4. Я бы выбрал Docker быстро собирается и не требует больших затрат по ресурсам, если брать более масштабируемые ВМ то тогда KVM или XEN.

### Задача 4

Опишите возможные проблемы и недостатки гетерогенной среды виртуализации (использования нескольких систем управления виртуализации одновременно) и что необходимо сделать для минимизации этих рисков и проблем. Если бы у вас был выбор, то создавали бы вы гетерогенную среду или нет? Мотивируйте ваш ответ примерами.

Проблемы гетерогенной среды:
- содержать несколько команд администрирования/сопровождения для разных систем (кадровые издержки)
- гораздо ниже масштабируемость, придется масштабировать 2(или более) системы, 
- сложность при выделении и управлении ресурсами
- финансовые затраты, так как необходимо содержать несколько систем одновременно (если считать платные версии)
- проблемы миграции между разными системами, + полное дублирование всей инфраструктуры под 2(или более) системы виртуализации

Как минимизировать:

В первую очередь перевести всю возможную виртуализацию на аппаратную, а дальше выбрать подходящий гиппервизор по навыкам команды и бюджету организации.

Я бы не создавал гетерогенную среду намеренно, но по моему мнению использование Docker на ВМ это уже геторогенная среда, а при создании приложений без этого никак.