# Tornado-IOT

- tornado 6.0.3
- aiopg 1.0.0
- SQLAlchemy 1.3.8
- aio-pika 6.1.2
- alembic 1.2.1
- aio-pika 6.1.2
- aioredis 1.3.0

###Getting started

 To run project:
 
```
docker-compose up -d
```
 
  Project already has own created migration. You need to apply this migration by command:
  
```
docker exec -it web alembic upgrade head
```

  If you wanna created your own migration with the updated or created tables:
  
```
docker exec -it web alembic revision --autogenerate -m "The name of migration"
```

To run tests:

```
docker exec -it web python manage.py test
```