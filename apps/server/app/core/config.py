#!/usr/bin/python3

import secrets
from typing import List
from functools import lru_cache
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings class
    """
    # Application
    APP_ENV: str = 'development'
    APP_NAME: str = "Plataforma de Eventos e Ingressos"
    APPL_VERSION: str = "1.0.0"
    API_V1_PATH: str = "/api/v1"

    # Security & JWT
    SECRET_KEY: str = ""
    JWT_SECRET_KEY: str = ""
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Database
    DATABASE_URL: str = ""
    DATABASE_POOL_SIZE: int = 5
    DATABASE_POOL_TIMEOUT: int = 30
    DATABASE_POOL_MAX_CONNECTIONS: int = 100
    DATABASE_MAX_OVERFLOW: int = 10
    DATABASE_POOL_PRE_PING: bool = True
    DATABASE_POOL_RECYCLE: int = 3600
    DATABASE_SQL_ECHO: bool = False

    # Redis
    REDIS_URL: str = ""

    # Environment
    DEBUG: bool = False

    # CORS
    CORS_ORIGIN: List[str] = ["http://localhost:5173"]

    # CATALOG
    TICKETMASTER_API_KEY:str | None = None


    # Validation for production
    @field_validator("DATABASE_URL")
    def validate_database_url(cls, v, values):
        if values.data.get("ENVIRONMENT") == "production" and "localhost" in v:
            raise ValueError("A URL da base de dados em produção não pode usar localhost")
        return v

    @field_validator("SECRET_KEY")
    def validate_secret_key(cls, v, values):
        if values.data.get("APP_ENV") == "production" and v == "changeme":
            raise ValueError("Deve atribuir o SECRET_KEY em ambiente de produção")
        return v

    @field_validator("CORS_ORIGIN", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        """Accept either JSON-style lists or comma-separated strings."""
        if not v:
            return []
        if isinstance(v, str):
            # Strip spaces and split commas
            return [i.strip() for i in v.split(",") if i.strip()]
        if isinstance(v, list):
            return v
        raise TypeError("Formato do CORS_ORIGIN inválido")

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    """ Returns cached application settings instance"""
    
    return Settings()
