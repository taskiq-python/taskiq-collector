import logging
from importlib import metadata
from pathlib import Path

import sentry_sdk
from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import PrometheusFastApiInstrumentator
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.logging import LoggingIntegration
from tortoise.contrib.fastapi import register_tortoise

from taskiq_collector.db.config import TORTOISE_CONFIG
from taskiq_collector.logging import configure_logging
from taskiq_collector.settings import settings
from taskiq_collector.web.api.router import api_router
from taskiq_collector.web.lifetime import (
    register_shutdown_event,
    register_startup_event,
)

APP_ROOT = Path(__file__).parent.parent


def get_app(enable_metrics: bool = True) -> FastAPI:  # noqa: WPS213
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :param enable_metrics: wether we want to enable prometheus.
    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title="taskiq_collector",
        description="Web application to collect taskiq data",
        version=metadata.version("taskiq_collector"),
        docs_url=None,
        redoc_url=None,
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    # Registers prometheus metrics.
    if enable_metrics:
        PrometheusFastApiInstrumentator(should_group_status_codes=False).instrument(
            app,
        ).expose(app, should_gzip=True, name="prometheus_metrics")

    # Adds static directory.
    # This directory is used to access swagger files.
    app.mount(
        "/swagger_static",
        StaticFiles(directory=APP_ROOT / "static/docs"),
        name="swagger_static",
    )
    app.mount(
        "/",
        StaticFiles(directory=APP_ROOT / "static/front", html=True),
        name="front",
    )

    # Configures tortoise orm.
    register_tortoise(
        app,
        config=TORTOISE_CONFIG,
        add_exception_handlers=True,
    )
    if settings.sentry_dsn:
        # Enables sentry integration.
        sentry_sdk.init(
            dsn=settings.sentry_dsn,
            traces_sample_rate=settings.sentry_sample_rate,
            environment=settings.environment,
            integrations=[
                LoggingIntegration(
                    level=logging.getLevelName(
                        settings.log_level.value,
                    ),
                    event_level=logging.ERROR,
                ),
            ],
        )
        app = SentryAsgiMiddleware(app)  # type: ignore

    return app
