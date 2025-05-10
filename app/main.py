from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.app import app_settings
from app.presentation.api.routes import api_router


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):  # noqa ARG001
    yield


app = FastAPI(
    title=app_settings.app_name,
    lifespan=lifespan,
    debug=app_settings.debug,
)
app.include_router(api_router)

