# Detele if Docker 
import uvicorn

# Main dependencies
from fastapi import FastAPI
import logging

from api import api_router
from config import get_app_settings


# Setup application
def get_application() -> FastAPI:
    
    settings = get_app_settings()
    app = FastAPI(**settings.fastapi_kwargs)
    
    app.add_event_handler(
        "startup",
        on_startup,
    )
    
    app.add_event_handler(
        "shutdown",
        on_shutdown,
    )
    
    app.include_router(api_router)
    
    return app


# Process startup events
def on_startup():
    pass

# Process startup events
def on_shutdown():
    pass


if __name__ == '__main__':
    app = get_application()
    uvicorn.run(app, host="localhost", port=3000)