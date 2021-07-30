from core.settings import Settings
from fastapi import FastAPI
from core.db import db


def create_app():
    app = FastAPI()

    config = Settings.load()

    db.init_app(app=app, **config)

    @app.get("/")
    def root():
        return {"message": "Hello World"}

    return app


app = create_app()
