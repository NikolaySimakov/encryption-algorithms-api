# Detele if Docker 
import uvicorn
import os

# Main dependencies
from fastapi import FastAPI
import logging

from api import api_router
from config import get_app_settings

from fastapi_sqlalchemy import DBSessionMiddleware, db

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
    
    app.add_middleware(DBSessionMiddleware, db_url=os.environ["DB_URL"])
    # app.add_middleware(DBSessionMiddleware, db_url="postgresql://postgres:postgres@localhost:5433/keydb")
    return app


# Process startup events
def on_startup():
    pass

# Process startup events
def on_shutdown():
    pass


app = get_application()

# if __name__ == '__main__':
#     app = get_application()
    # uvicorn.run(app, host="api", port=3000)