from fastapi import APIRouter

movie_router = APIRouter()


@movie_router.get("/")
def read_movie():
    return [{"title": "Kingdom"}, {"title": "The Crown"}]
