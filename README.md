

### Стэк технологий и фреймворков

* [Python 3.7](https://docs.python.org/3/)
* [Tarantool](https://www.tarantool.io/en/developers/)
* [aiohttp](https://aiohttp.readthedocs.io/en/stable/)
* [jsonschema](https://pypi.org/project/jsonschema/)
* [numpy](https://www.numpy.org)
* [Docker](https://docs.docker.com/v17.09/)

### Структура приложения

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
        |__ service.py - содержит функции, которые выполняется для подготовки ответа, например, работа с базой, маппинг данных или некоторые расчеты (numpy, ...)
    |__ utils
        |__ check_consistency.py - функция для проверки валидности данных в импорте
        |__ helper.py - содержит некоторые вспомогателные функции, такие как конвертация из словаря в кортеж и тп
        |__ sort.py - настройка для сортировки
        |__ validation.py - расширение валидации
    |__ Dockerfile - docker-файл для создания образа с приложением
|   
|__ tarantool
    |__app.lua - конфигурационный файл для задания настроек tarantool и определения хранимых процедур
    |__Dockerfile - docker-файл для создания образа с нужными настройками
    
docker-compose.yml - описания сервисов для создания образов и запуска контейнеров посредством утилиты docker-compose 

### CI/CD

Для деплоя приложения используется docker и docker hub.

#### Текущий Workflow
* $ docker-compose build - создает два образа: project_name_prefix_tarantool и project_name_prefix_web
* ~~$ docker-compose up -d - запускает контейнеры на основе созданных образов~~
* docker tag project_name_prefix_service docker_hub_repo:service_name // service_name = web, tarantool
* (on server) docker login
* (on server) docker pull docker_hub_repo:service_name // service_name = web, tarantool
* (on server) sudo docker run -d -p3301:3301--name tarantool --network='mynet' docker_hub_repo:service_name // service_name = web, tarantool


### Задачи
- [x] подключить docker
- [x] настроить Dockerfile app
- [x] настроить Dockerfile tarantool
- [ ] донастроить docker-compose
- [ ] добавить тесты

### Нерешенные проблемы
- [ ] docker-compose при создании контейнеров создает их или с неверным алиасом для network или вообще без него, вследствии чего обращение от сервера к базе по алиасу tarantool невозможно и сервер не стартует

