from os import environ
from typing import List
from pydantic import BaseSettings


class EnvSettings(BaseSettings):
    JWT_SECRET_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class GlobalSettings(BaseSettings):
    DB_URL: str
    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True
    PROJ_RELOAD: bool = True
    TRUSTED_HOST: List[str] = ["*"]
    ALLOW_SITE: List[str] = ["*"]

    class Config:
        env_file = ".env.local"
        env_file_encoding = "utf-8"


class LocalSettings(GlobalSettings):
    class Config:
        env_file = ".env.local"


class TestSettings(GlobalSettings):
    PROJ_RELOAD = False

    class Config:
        env_file = ".env.test"


class ProdSettings(GlobalSettings):
    PROJ_RELOAD = False

    class Config:
        env_file = ".env.prod"


class Settings:
    @staticmethod
    def load():
        api_env = environ.get("API_ENV", "local")
        if api_env == "prod":
            return ProdSettings().dict()
        if api_env == "test":
            return TestSettings().dict()
        return LocalSettings().dict()


class Env:
    @staticmethod
    def load():
        return EnvSettings().dict()


if __name__ == "__main__":
    import json

    config = Settings.load()
    env = Env.load()
    api_env = environ.get("API_ENV", "local")
    print(f"----- Current ENV : {api_env} -----\n")
    print("----- Current Config Options -----")
    print(json.dumps(config, indent=4), end="\n\n")
    print("----- Current Env List -----")
    print(json.dumps(env, indent=4))
