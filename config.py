import os
from dotenv import load_dotenv

load_dotenv()  # safe but harmless if called multiple times


class Config:
    """Base configuration"""

    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///dilse.db'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False

    # IMPORTANT: do NOT freeze API key at import time
    @staticmethod
    def GEMINI_API_KEY():
        return os.getenv("GEMINI_API_KEY")

    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}