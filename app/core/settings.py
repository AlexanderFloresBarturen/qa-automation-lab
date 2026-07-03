import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()


class DatabaseEnvironment(str, Enum):
    DEVELOPMENT = "development"
    TEST = "test"


class Settings:
    # region Database
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT: int = int(os.getenv("DATABASE_PORT", "5432"))
    DATABSE_USER: str = os.getenv("DATABASE_USER", "postgres")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "postgres")
    DEVELOPMENT_DATABASE_NAME: str = os.getenv("DEVELOPMENT_DATABASE_NAME", "users")
    TEST_DATABASE_NAME: str = os.getenv("TEST_DATABASE_NAME", "users_test")

    CURRENT_DATABASE: DatabaseEnvironment = DatabaseEnvironment.DEVELOPMENT
    
    # endregion

    # region Database URLs
    @property
    def DEVELOPMENT_DATABASE_URL(self) -> str:
        return f"postgresql+psycopg://{self.DATABSE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DEVELOPMENT_DATABASE_NAME}"

    @property
    def TEST_DATABASE_URL(self) -> str:
        return f"postgresql+psycopg://{self.DATABSE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.TEST_DATABASE_NAME}"
    
    # endregion

    # region JWT
    SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION"

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15

    # endregion

    # region Authentication
    MAX_LOGIN_ATTEMPTS: int = 5

    ACCOUNT_LOCK_MINUTES: int = 15

    # endregion

    # region Password Recovery
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES: int = 15

    # endregion

    def __init__(self) -> None:
        self.DATABASE_URL = self.DEVELOPMENT_DATABASE_URL

    # region Helpers
    def use_development_database(self) -> None:
        self.DATABASE_URL = self.DEVELOPMENT_DATABASE_URL
        self.CURRENT_DATABASE = DatabaseEnvironment.DEVELOPMENT

    def use_test_database(self) -> None:
        self.DATABASE_URL = self.TEST_DATABASE_URL
        self.CURRENT_DATABASE = DatabaseEnvironment.TEST

    # endregion

    # region Properties
    @property
    def is_development_database(self) -> bool:
        return self.CURRENT_DATABASE == DatabaseEnvironment.DEVELOPMENT

    @property
    def is_test_database(self) -> bool:
        return self.CURRENT_DATABASE == DatabaseEnvironment.TEST

    # endregion

    def __repr__(self) -> str:
        return f"Settings(database={self.CURRENT_DATABASE}, url={self.DATABASE_URL})"


settings = Settings()
