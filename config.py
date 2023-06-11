from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os

load_dotenv()

APP_NAME = os.getenv("APP_NAME")
APP_VERSION = os.getenv("APP_VERSION")
APP_DESC = os.getenv("APP_DESC")

SQLITE_BASE_URL = os.getenv("SQLITE_BASE_URL")

BASE_DIR = os.getcwd()
STATIC_DIR = "static"
TEMPLATE_DIR = "templates"


def create_app() -> FastAPI:
    app = FastAPI(
        title=APP_NAME,
        description=APP_DESC,
        version=APP_VERSION,
        docs_url="/",
    )
    mount_app(app)
    return app


def mount_app(app: FastAPI) -> None:
    app.mount("/static", StaticFiles(directory="static"), name="static")


def register_router(app: FastAPI) -> None:
    pass
