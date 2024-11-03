from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    token_expiry: int
    db_name: str
    db_hostname: str
    db_port: str
    db_password: str
    db_username: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
