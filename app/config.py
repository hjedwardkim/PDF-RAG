from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    azure_openai_key: str
    azure_openai_endpoint: str
    azure_openai_embedding_deployment: str
    azure_openai_llm_deployment: str
    postgres_user: str
    postgres_password: str
    postgres_db: str
    db_host: str = "db"
    db_port: str = "5432"

    class Config:
        env_file = ".env"


settings = Settings()
