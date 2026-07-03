from enum import Enum


class DatabaseEnvironment(str, Enum):
    DEVELOPMENT = "development"
    TEST = "test"


class Settings:
    # region Database
    DEVELOPMENT_DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@192.168.56.2:5432/users"

    TEST_DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@192.168.56.2:5432/users_test"

    DATABASE_URL: str = DEVELOPMENT_DATABASE_URL

    CURRENT_DATABASE: DatabaseEnvironment = DatabaseEnvironment.DEVELOPMENT

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
