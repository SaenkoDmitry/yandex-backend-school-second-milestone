

### Стэк технологий и фреймворков

* [Python 3.7](https://docs.python.org/3/)
* [Tarantool](https://www.tarantool.io/en/developers/)
* [aiohttp](https://aiohttp.readthedocs.io/en/stable/)
* [jsonschema](https://pypi.org/project/jsonschema/)
* [numpy](https://www.numpy.org)
* [Docker](https://docs.docker.com/v17.09/)

### Структура приложения

```

|
|__ app
    |__ db
        |__ tarantool.py - создает подключение к базе tarantool и space-у 'citizens'
    |__ routes
        |__ routes.py - определяет ендпоинты, которые способен обработать сервер
    |__ schema
        |__ rest.py - определены схемы для валидации входящих запросов к серверу
        |__ tarantool.py - содержит кортеж (схему) для маппинга ответа из базы на структуры python
    |__ service
        |__ service.py - содержит функции, которые выполняется для подготовки ответа, например, работа с базой, 
        маппинг данных или некоторые расчеты (numpy, ...)
    |__ utils
        |__ check_consistency.py - функция для проверки валидности данных в импорте
        |__ helper.py - содержит некоторые вспомогателные функции, такие как конвертация из словаря в кортеж и тп
        |__ sort.py - настройка для сортировки
        |__ validation.py - расширение валидации
    |__ Dockerfile - docker-файл для создания образа с приложением
    |__ requirements.txt - описание зависимостей приложения и их версий
    |__ run.py - импорт модуля app
|   
|__ tarantool
    |__app.lua - конфигурационный файл для задания настроек tarantool и определения хранимых процедур
    |__Dockerfile - docker-файл для создания образа с нужными настройками
    
docker-compose.yml - описания сервисов для создания образов и запуска контейнеров посредством утилиты docker-compose
    
```

### База данных

В качестве базы данных был выбран tarantool по причине его высокой производительности при решении задач на чтение и запись данных, 
а также удобства написания и использования хранимых процедур на языке lua

### CI/CD

Для деплоя приложения используется docker и docker hub.

#### Текущий Workflow
1. перейти в директорию ansible проекта и подставить в файл playbook.yml значение переменной с указанием пути к проекту
2. выполнить ansible-playbook скрипт для отправки исходников на сервер, запустив команду:
```
ansible-playbook -i environments playbook.yml
```

3. $ (на удаленной машине) перейти в папку /home/entrant/gifts и выполнить команду:
```
sudo docker-compose build - создает два образа: gifts_tarantool и gifts_web
```

4. (на удаленной машине) выполнить команды для запуска сервисов в представленной ниже очередности:
```
sudo docker run -d --restart unless-stopped -p 3301:3301 --name tarantool --network='mynet' gifts_tarantool
sudo docker run -d --restart unless-stopped -p 8080:8080 --name web --network='mynet' gifts_web
```


### Задачи
- [x] подключить docker
- [x] настроить Dockerfile app
- [x] настроить Dockerfile tarantool
- [ ] донастроить docker-compose
- [ ] добавить тесты

### Нерешенные проблемы
- [ ] docker-compose при создании контейнеров создает их с неверным алиасом для network, вследствии чего обращение от сервера к базе по алиасу tarantool невозможно и сервер не стартует
(временное решение: использовать docker-compose только для создания образов, запускать контейнеры вручную)
