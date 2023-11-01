## Highlights of the Current Codebase

### Docker Integration:
* The application, along with Nginx, is containerized,
  ensuring consistent environments across deployment stages.
### Database Version Control with Alembic:
* Smoothly track and manage database schema changes using Alembic,
  ensuring consistent database states.
### Compliance with the 12 Factor App Principles:
* The solution aligns with the 12 Factor App methodology [https://12factor.net].
  It's designed for microservice deployment and is built to scale efficiently.


## Requirements
* FastAPI
* PostgresSQL
* Docker (optional)

## Setup instructions

* create virtual environment
```
virtualenv <name of your env>
```
* Activate environment
```
source <path to your env>/bin/activate
```
* Setup virtual env
```
pipenv install
```


* Make sure the DB connections are correct in the config.py
```
postgresql://postgres:postgres@localhost:5432/seek
```
* Run the app

```
* uvicorn main:app --reload
```
* Access Swagger at
```
http://127.0.0.1:5000/docs
```
* run tests (in root folder)
```
pytest
```



## Alternative instructions for Docker

* Make sure the DB connections are correct in the env
```
postgresql://postgres:postgres@host.docker.internal:5432/seek
```
* Run the docker container by issuing
```
docker-compose --build
```
* Access Swagger at
```
http://127.0.0.1/docs
```

## Missing
- azure funcs
- concurrency errors
- postgres db container
- download actual files using the get API
- other endpoints (edit)
