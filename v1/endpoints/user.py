from fastapi import APIRouter


user_router = APIRouter()


@user_router.get("/", description="Userrrrr", summary="AAAAA")
def read_user():
    return [{"username": "Rick"}, {"username": "Morty"}]


@user_router.post("/register")
def register_user():
    return ""


@user_router.post("/login")
def login():
    return ""


@user_router.post("/edit")
def edit_profile():
    return ""
