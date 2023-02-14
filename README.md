# Cookiecutter FastAPI

> Cookiecutter template for FastAPI

![](https://github.com/wonyoungseo/cookiecutter-fastapi/blob/main/images/example_api_screenshot.png)

## 0. Prerequisite

1. Python must be installed on your OS
2. Cookiecutter must be installed

[Reference guide on installation](https://cookiecutter.readthedocs.io/en/2.1.1/installation.html#)

## 1. Project template structure

```text
.
├── README.md
├── .env
├── app.py
├── src
│   ├── __init__.py
│   ├── data_models
│   │   └── __init__.py
│   ├── modules
│   │   └── __init__.py
│   ├── routers
│   │   ├── __init__.py
│   │   └── hello_world.py
│   ├── services
│   │   └── __init__.py
│   ├── settings.py
│   └── utils
│       ├── __init__.py
│       └── logger_utils.py
├── configs
│   └── logging
│       └── logging_config.yaml
├── logs
├── test
│   ├── __init__.py
│   └── test_api.py
├── requirements.txt
├── Dockerfile
└── .gitignore
```

- `.env`: global configs for server itself.
- `app.py`: entrypoint for API. contains no logic
- `src`: directory for all API related codes
  - `routers`: API routers(handling requests). Does not contain any business logics, and only serve as router.
  - `data_models`: data model defined with `pydantic`
  - `services`: all processing and business logics for routers
  - `modules`: modular codes to support business logics inside services layer
  - `settings.py`: loader for configs and settings
  - `utils`: utility codes
- `configs`: directory all configuration of the applications.
- `logs`: directory where log files are stored 
- `test`: test cases for API
- `requirements.txt`: list of dependencies for the API application 
- `Dockerfile`: Dockerfile to build image of the API application

## 2. Generate FastAPI project via `cookiecutter`

Command can be either one of the followings;

```bash
# With URL
$ cookiecutter https://github.com/wonyoungseo/cookiecutter-fastapi.git

# With Github user name and repository name
$ cookiecutter gh:wonyoungseo/cookiecutter-fastapi
```

## 3. Run FastAPI app

```bash
# With pip
$ pip install -r requirements.txt
$ python app.py
```

```bash
# With Docker
$ docker build -t fastapi_app .
$ docker run -rm  -p 8000:8000 fastapi_app
```
