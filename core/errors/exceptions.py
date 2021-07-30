class StatusCode:
    HTTP_500 = 500
    HTTP_400 = 400
    HTTP_401 = 401
    HTTP_403 = 403
    HTTP_404 = 404
    HTTP_405 = 405
    HTTP_409 = 409


class APIException(Exception):
    status_code: int
    code: str
    msg: str
    detail: str

    def __init__(
        self,
        *,
        status_code: int = StatusCode.HTTP_500,
        code: str = "000000",
        msg: str = None,
        detail: str = None,
        ex: Exception = None,
    ):
        self.status_code = status_code
        self.code = code
        self.msg = msg
        self.detail = detail

        super().__init__(ex)


class NotFoundUserEx(APIException):
    def __init__(self, user_id: int, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_404,
            code=f"{StatusCode.HTTP_404}{'1'.zfill(4)}",
            msg=f"해당 유저를 찾을 수 없습니다.",
            detail=f"Not Found User ID: {user_id}",
            ex=ex,
        )


class NotAuthorized(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            code=f"{StatusCode.HTTP_401}{'1'.zfill(4)}",
            msg=f"로그인이 필요한 서비스입니다.",
            detail=f"Authorization Required",
            ex=ex,
        )


class TokenDecodeEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            code=f"{StatusCode.HTTP_400}{'2'.zfill(4)}",
            msg=f"비정상적인 접근입니다.",
            detail=f"Token has been compromised",
            ex=ex,
        )


class PasswordFailed(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            code=f"{StatusCode.HTTP_400}{'3'.zfill(4)}",
            msg=f"동일한 비밀번호를 입력해주세요.",
            detail=f"Invalid Password",
            ex=ex,
        )


class ExistEmail(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_409,
            code=f"{StatusCode.HTTP_409}{'0'.zfill(4)}",
            msg=f"이미 가입된 이메일입니다.",
            detail=f"Exist Email",
            ex=ex,
        )
