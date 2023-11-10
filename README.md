# api-rick-and-morty

---

### Requirement:

1. Endpoint, which return random character from the world of Rick and Morty series.
2. Endpoint get search_string as an argument and return list of all characters, who contains the search_string  in the name.
3. On regular basis, pp downloads data from external service inner DB.
4. Requests of implemented API should work with local DB (Take data from DB not from Rick & Morty API).

Technologies to use:

1. Public API https://rickandmortyapi.com/documentation/.
2. Use Celery as task scheduler for data synchronization for Rick & Morty API.
3. Python, Django/Flask/FastAPI, ORM, PostgreSQL, GIT
4. All endpoints should be documented via Swagger.

---

## preconditions:

## - git and docker must be installed


## Clone project:

```bash
git clone https://github.com/KonstZiv/api-rick-and-morty.git
cd api-rick-and-morty
```

## Start project

```bash
$ docker-compose up --build
```

## Resources are available within the project:

- API endpoints:
    - http://127.0.0.1:8000/api/v1/characters/random/
    - http://127.0.0.1:8000/api/v1/characters/
- documentation (Swagger) - http://127.0.0.1:8000/api/v1/doc/swagger/
- administrative panel (superuser access) - http://127.0.0.1:8000/admin/
- task control panel (Flower) - http://127.0.0.1:5555/