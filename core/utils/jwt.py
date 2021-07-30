import jwt
from core.settings import Env


def encode_jwt(payload) -> str:
    env = Env.load()
    return jwt.encode(payload, env.get("JWT_SECRET_KEY"), algorithm="HS256")


def verify_jwt(token: str):
    env = Env.load()
    return jwt.decode(token, env.get("JWT_SECRET_KEY"), algorithms=["HS256"])
