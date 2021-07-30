from fastapi import APIRouter
from v1.endpoints import user_router, movie_router


class V1:
    @staticmethod
    def load():
        v1_router: APIRouter = APIRouter()
        v1_router.include_router(movie_router, prefix="/movie", tags=["Movie"])
        v1_router.include_router(user_router, prefix="/user", tags=["User"])
        return v1_router
