import time
import typing
import re

from jwt.exceptions import PyJWTError

from core.utils.jwt import verify_jwt
from core.errors import exceptions as ex
from core.errors.exceptions import APIException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.datastructures import Headers
from starlette.types import ASGIApp, Receive, Scope, Send


class AccessControl:
    def __init__(
        self,
        app: ASGIApp,
        except_path_list: typing.Sequence[str] = None,
        except_path_regex: str = None,
    ) -> None:
        if except_path_list is None:
            except_path_list = ["*"]

        self.app = app
        self.except_path_list = except_path_list
        self.except_path_regex = except_path_regex

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        request = Request(scope=scope)
        headers = Headers(scope=scope)

        request.state.start = time.time()
        request.state.inspect = None
        request.state.user = None
        request.state.is_admin_access = None

        ip = (
            request.headers["x-forwarded-for"]
            if "x-forwarded-for" in request.headers.keys()
            else request.client.host
        )
        request.state.ip = ip.split[","][0] if "," in ip else ip

        if await (
            self.url_pattern_check(request.url.path, self.except_path_regex)
            or request.url.path in self.except_path_list
        ):
            return await self.app(scope, receive, send)

        try:
            if request.url.path.startswith("/api"):
                if "authorization" in request.headers.keys():
                    token_info = await self.token_decode(
                        access_token=request.headers.get("Authorization")
                    )
                    # TODO: UserToken 모델을 만들어야 함
                    request.state.user = token_info
                else:
                    raise ex.NotAuthorized()
            else:
                if "authorization" not in request.cookies.keys():
                    raise ex.NotAuthorized()

                request.state.user = await self.token_decode(
                    access_token=request.cookies.get("Authorization")
                )

            # TODO: Date Util을 만들어야 함
            # request.state.req_time = D.datetime()
            res = await self.app(scope, receive, send)

        except APIException as e:
            res = await self.exception_handler(e)
            res = await res(scope, receive, send)

        finally:
            pass

        return res

    @staticmethod
    async def url_pattern_check(path, pattern):
        result = re.match(pattern, path)
        return bool(result)

    @staticmethod
    async def token_decode(access_token):
        try:
            access_token = access_token.replace("Bearer ", "")
            payload = verify_jwt(access_token)
            return payload
        except PyJWTError as e:
            print(e)

    @staticmethod
    async def exception_handler(error: APIException):
        error_dict = dict(
            status=error.status_code,
            msg=error.msg,
            detail=error.detail,
            code=error.code,
        )
        res = JSONResponse(status_code=error.status_code, content=error_dict)
        return res
