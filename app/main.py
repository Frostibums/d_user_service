from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.app import app_settings
from app.config.kafka import kafka_settings
from app.infrastructure.bus.kafka.producer import KafkaEventProducer
from app.presentation.api.routes import api_router


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):  # noqa ARG001
    kafka_producer = KafkaEventProducer(
        bootstrap_servers=kafka_settings.bootstrap_servers,
    )
    await kafka_producer.start()
    fastapi_app.state.kafka_producer = kafka_producer

    yield

    await kafka_producer.stop()


app = FastAPI(
    title=app_settings.app_name,
    lifespan=lifespan,
    debug=app_settings.debug,
)
app.include_router(api_router)

