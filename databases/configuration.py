from typing import Optional

from pydantic import BaseSettings
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config import APP_NAME, APP_VERSION, SQLITE_BASE_URL
import os


class Settings(BaseSettings):
    APP_NAME: str = APP_NAME
    APP_VERSION: str = APP_VERSION
    DATABASE_FOLDER: Optional[str] = "storages"
    DATABASE_NAME: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.DATABASE_FOLDER and self.DATABASE_FOLDER not in os.listdir():
            os.makedirs(self.DATABASE_FOLDER, exist_ok=True)

    @property
    def get_db_url(self) -> str:
        return f"{SQLITE_BASE_URL.rstrip('/')}/{self.DATABASE_FOLDER}/"


class DatabaseManager:
    def __init__(self, base_db_url: str, settings: Settings):
        self.base_engine = self.create_engine(base_db_url)
        self.settings = settings
        self.engines = {"base": self.base_engine}

    @staticmethod
    def create_engine(db_url: str) -> Engine:
        return create_engine(db_url, connect_args={"check_same_thread": False})

    def get_engine(self, db_url: str) -> Engine:
        """
        Get the engine for the session

        Arg:
        db_url: str
        For example: db_url = sqlite:///./storage/db.sqlite
        """
        if db_url in self.engines:
            return self.engines[db_url]

        engine = self.create_engine(db_url)
        self.engines[db_url] = engine
        return engine

    def get_db(self, db_url: Optional[str] = None):
        """
        Get the database session

        Yields:
            Session: The database session
        """
        if db_url is None:
            engine = self.base_engine
        else:
            engine = self.get_engine(db_url)

        session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
        try:
            yield session
        finally:
            session.close()


Base = declarative_base()
settings = Settings(DATABASE_NAME="sqlite.db")
db_manager = DatabaseManager(settings.get_db_url, settings)

# db_url = 'sqlite:///db1.sqlite3'
# with db_manager.get_db(db_url) as session:
# Perform database operations using the session connected to the specified database
# For example:
# result = session.query(MyModel).all()
