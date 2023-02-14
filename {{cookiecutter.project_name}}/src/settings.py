from pathlib import Path
from typing import Optional
from pydantic import Field, BaseSettings, BaseModel


class AppEnv(BaseModel):
    """Application configurations."""
    # all the directory level information defined at app config level
    # we do not want to pollute the env level config with these information
    # this can change on the basis of usage

    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    LOGS_DIR: Path = BASE_DIR.joinpath('logs')
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    # configs
    CONFIGS_DIR: Path = BASE_DIR.joinpath('configs')
    CONFIGS_DIR.mkdir(parents=True, exist_ok=True)

    LOGGING_CONFIGS_DIR: Path = CONFIGS_DIR.joinpath('logging')
    LOGGING_CONFIGS_DIR.mkdir(parents=True, exist_ok=True)

class GlobalEnv(BaseSettings):
    """Global configurations."""
    # These variables will be loaded from the .env file. However, if
    # there is a shell environment variable having the same name,
    # that will take precedence.

    # define global variables with the Field class
    ENV_STATE: str = Field(None, env="ENV_STATE")

    # Application Config
    APP_ENV: AppEnv = AppEnv()

    # API info
    API_NAME: str = Field(None, env="API_NAME")
    API_VERSION: str = Field(None, env="API_VERSION")
    API_DESCRIPTION: str = Field(None, env="API_DESCRIPTION")
    API_DEBUG_MODE: bool = Field(None, env="API_DEBUG_MODE")

    # basic api settings
    HOST: str = None
    PORT: int = None
    LOG_LEVEL: str = None

    ### FILENAME ###
    # config file name - API
    CONFIG_LOGGING_FILENAME: str = Field(None, env="CONFIG_LOGGING_FILENAME")

    class Config:
        env_file: str = ".env"
        env_file_encoding = "utf-8"


class DevEnv(GlobalEnv):
    class Config:
        env_prefix: str = "DEV_"


class ProdEnv(GlobalEnv):
    class Config:
        env_prefix: str = "PROD_"


class FactoryEnv:

    def __init__(self, env_state: Optional[str]):
        self.env_state = env_state

    def __call__(self):
        if self.env_state == "DEV":
            return DevEnv()

        elif self.env_state == "PROD":
            return ProdEnv()

        else:
            raise ValueError("invalid env_state: {}".format(self.env_state))


settings = FactoryEnv(GlobalEnv().ENV_STATE)()