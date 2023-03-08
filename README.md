![status badge](https://github.com/skhamatulin/foodgram-project-react/actions/workflows/main.yml/badge.svg)


#Foodgram, «Продуктовый помощник».

#### Пример развернутого проекта можно посмотреть [здесь](http://158.160.8.22/)

##Технологии
```
python==3.7
Django==3.2.18
djangorestframework==3.12.4
PostgreSQL
docker
```

## Особенности
Проект запускается в четырёх контейнерах
```
nginx:1.19.3
foodgram-backend:v1.0.0
foodgram-frontend:v1.0.0
postgres:12.4
```

foodgram-frontend:v1.0.0 используется только для сборки, далее работает через nginx

# Запуск
1) Клонировать репозиторий
2) В папке infra создать .env и заполнить дефолтными значениями
```
DB_ENGINE=django.db.backends.postgresql_psycopg2
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
3) В папке infra выполнить
```
docker-compose up -d --build
```

4) Сделать миграции, собрать статику и создать суперпользователя:
```
docker-compose exec -T web python manage.py makemigrations users
docker-compose exec -T web python manage.py makemigrations recipes
docker-compose exec -T web python manage.py migrate
docker-compose exec -T web python manage.py collectstatic --no-input
docker-compose exec web python manage.py createsuperuser
```

5) Заполнить БД тестовыми записями:
открыть bash
```
docker-compose exec backend bush
```
выгрузить данные из дампа
```
python manage.py loaddata fixtures.json
```
