from fastapi import FastAPI
from .api.users.router import user_router


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(router=user_router)
    return application

app = create_application()