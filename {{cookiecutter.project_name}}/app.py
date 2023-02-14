from pathlib import Path
import json
import logging
from loguru import logger

import uvicorn
from starlette.types import Message
from fastapi import FastAPI, Request

from src.routers.hello_world import router as router_hello_world

from src.settings import settings
from src.utils.logger_utils import setup_logging

APP_LOG_LEVEL = logging.getLevelName(settings.LOG_LEVEL)


async def set_body(request: Request, body: bytes):
    async def receive() -> Message:
        return {"type": "http.request", "body": body}

    request._receive = receive


async def middleware_logging(request: Request, call_next):
    logger.info('Request from {}:{} - "{} {}"'.format(request.client.host,
                                                      request.client.port,
                                                      request.method,
                                                      request.url))

    if str(request.method) in ['POST', 'PUT', 'PATCH']:
        body = await request.body()
        await set_body(request, body)
        request_body = json.loads(body)
        logging.info("Request Body :")
        for k in request_body:
            logging.info("\t{}".format({k: request_body[k]}))

    response = await call_next(request)
    return response


def get_application():
    app = FastAPI(title=settings.API_NAME,
                  version=settings.API_VERSION,
                  description=settings.API_DESCRIPTION)

    app.middleware("http")(middleware_logging)
    app.include_router(router_hello_world, tags=['say_hello_world'])

    return app


app = get_application()

if __name__ == "__main__":
    assert settings.ENV_STATE in ['DEV', 'PROD'], "ENV_STATE must be one of ['DEV', 'PROD']"
    log_level: dict = {"DEV": {"reload": True, "uvicorn_log_level": "DEBUG"},
                       "PROD": {"reload": False, "uvicorn_log_level": "CRITICAL"}}

    reload = log_level[settings.ENV_STATE]['reload']
    uvicorn_log_level = log_level[settings.ENV_STATE]['uvicorn_log_level']
    setup_logging(log_level=APP_LOG_LEVEL)
    logger.info("Uvicorn running on http://{}:{} (Press CTRL+C to quit)".format(settings.HOST, settings.PORT))

    uvicorn.run("app:app",
                host=settings.HOST,
                port=settings.PORT,
                log_config=str(Path.joinpath(settings.APP_ENV.LOGGING_CONFIGS_DIR, settings.CONFIG_LOGGING_FILENAME)),
                log_level=logging.getLevelName(uvicorn_log_level),
                use_colors=True,
                reload=False,
                timeout_keep_alive=600,
                workers=1
                )
