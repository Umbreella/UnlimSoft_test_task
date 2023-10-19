# UnlimSoft (REST-API)

## Backend

![python](https://img.shields.io/badge/python-3776AB?logo=python&logoColor=white&style=for-the-badge&)
![fastapi](https://img.shields.io/badge/fastapi-009688?logo=fastapi&logoColor=white&style=for-the-badge&)
![sqlalchemy](https://img.shields.io/badge/sqlalchemy_+_alembic-d71f00?logo=sqlite&logoColor=white&style=for-the-badge&)
![poetry](https://img.shields.io/badge/poetry-60A5FA?logo=poetry&logoColor=white&style=for-the-badge&)

## Testing

![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
[![codecov](https://img.shields.io/codecov/c/github/Umbreella/UnlimSoft_test_task?&style=for-the-badge&logo=codecov)](https://codecov.io/gh/Umbreella/UnlimSoft_test_task)

## Database

![postgresql](https://img.shields.io/badge/postgresql-4169E1?logo=postgresql&logoColor=white&style=for-the-badge&)

## Cloud & CI/CD

![docker](https://img.shields.io/badge/docker-2496ED?logo=docker&logoColor=white&style=for-the-badge&)
![githubactions](https://img.shields.io/badge/githubactions-2088FF?logo=githubactions&logoColor=white&style=for-the-badge&)

---

## Description

[Task Description](TaskDescription.md)

## Getting Started

### Environment variables

To run the application, you need to set all the environment variables:

* **[.env.fastapi](.env)**
* **[.env.postgres](https://github.com/docker-library/docs/blob/master/postgres/README.md#environment-variables)**
    * POSTGRES_PASSWORD

## Docker

1. [docker-compose.yaml](docker-compose.yml)

```yaml
version: "3.8"

services:
  unlimsoft_test_task:
    image: umbreella/unlimsoft_test_task:latest
    container_name: unlimsoft_test_task
    restart: always
    ports:
      - 8000:8000
    environment:
      - APP_POSTGRES_USERNAME=postgres
      - APP_POSTGRES_PASSWORD=password
      - APP_POSTGRES_DB=testcrt
      - APP_POSTGRES_HOST=postgres13
    depends_on:
      - postgres
    networks:
      backend:

  postgres:
    image: postgres:13-alpine
    container_name: postgres
    restart: always
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=testcrt
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      backend:


volumes:
  postgres_data:

networks:
  backend:
```

2. Docker-compose run

```commandline
docker-compose up -d
```

3. Open bash in container

```commandline
docker exec -it unlimsoft_test_task bash
```

4. Run migrations

```commandline
alembic upgrade head
```

## Endpoints

* REST-API Docs

```
[your_ip_address]/api/docs/
```
