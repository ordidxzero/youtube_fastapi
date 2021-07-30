from fastapi import APIRouter


user_router = APIRouter()


@user_router.get("/")
def read_user():
    return [{"username": "Rick"}, {"username": "Morty"}]
