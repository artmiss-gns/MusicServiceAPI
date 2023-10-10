from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings) :
    DATABASE_URL: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    SECRET_KEY: str

    TEST_DATABASE_NAME: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
