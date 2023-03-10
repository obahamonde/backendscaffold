"""Application Settings"""

from json import loads

from pydantic import BaseSettings, Field, BaseConfig

GOOGLE_CREDENTIALS = loads(open("credentials.json", "r", encoding="utf-8").read())

class Settings(BaseSettings):

    """Environment variables"""

    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    AMQP_URL: str = Field(..., env="AMQP_URL")
    AWS_ACCESS_KEY_ID: str = Field(..., env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = Field(..., env="AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = Field(..., env="AWS_REGION")
    REDIS_PASSWORD: str = Field(..., env="REDIS_PASSWORD")
    REDIS_HOST: str = Field(..., env="REDIS_HOST")
    REDIS_PORT: int = Field(..., env="REDIS_PORT")
    GOOGLE_CREDENTIALS: dict = Field(default=GOOGLE_CREDENTIALS, env="GOOGLE_CREDENTIALS")


    class Config(BaseConfig):

        """Base config"""

        env_file = ".env"
        file_encoding = "utf-8"


env = Settings()
