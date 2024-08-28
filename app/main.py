from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from .api.auth.router import user_router
from .core.config import api_settings


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


def create_application() -> FastAPI:
    application = FastAPI(
        title=api_settings.PROJECT_NAME,
        description=f"${api_settings.PROJECT_NAME} server",
        custom_generate_unique_id=custom_generate_unique_id,
    )

    if api_settings.BACKEND_CORS_ORIGINS:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=[
                str(origin).strip("/") for origin in api_settings.BACKEND_CORS_ORIGINS
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    application.include_router(router=user_router, prefix=api_settings.API_V1_STR)
    return application


app = create_application()
