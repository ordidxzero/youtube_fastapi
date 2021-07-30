import uvicorn
from core.settings import Settings
from fastapi import FastAPI
from core.db import db
from v1 import V1


def create_app():
    app = FastAPI()

    config = Settings.load()

    db.init_app(app=app, **config)

    v1_router = V1.load()

    app.include_router(v1_router, prefix="/api/v1")

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
