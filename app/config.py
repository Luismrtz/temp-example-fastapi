from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"
#storing the variables after pydantic verifies these,
settings = Settings()

# print(settings.database_password)

# make sure to include in gitignore:::
# __pycache__ 
# venv/ 
# .env