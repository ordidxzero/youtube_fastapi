# FastAPI 프로젝트 구조

```bash
youtube_fastapi
├── main.py
├── core
│   ├── models
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── conn.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── v1
│   │       └── __init__.py
│   ├── schemas
│   │   ├── __init__.py
│   │   ├── schema.py
│   │   └── v1
│   │       └── __init__.py
│   └── settings.py
├── tests
│   ├── __init__.py
│   └── v1
│       └── __init__.py
└── v1
    ├── api.py
    ├── endpoints
    │   ├── endpoint.py
    │   └── __init__.py
    └── __init__.py 

```

[StackOverFlow](https://stackoverflow.com/questions/64943693/what-are-the-best-practices-for-structuring-a-fastapi-project) 및 [블로그](https://dingrr.com/blog/post/python-fastapi-%EB%A1%9C-%EB%B0%B1%EC%97%94%EB%93%9C-%EB%A7%8C%EB%93%A4%EA%B8%B0-2%ED%99%94-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%EA%B5%AC%EC%A1%B0)를 참고했습니다.

`core/db` : 데이터베이스를 세팅하는 파일들이 들어갑니다.

`core/settings.py` : Pydantic의 Settings Management에 매우 유용하며, 동일한 변수를 재선언하지 않고 사용할 수 있습니다. 설정 및 환경 변수에 대한 설명서를 확인하는 것이 유용할 수 있습니다.

`tests` : 테스트 코드가 들어갑니다.

`v1` : v1 endpoint들이 들어갑니다. `v1/api.py`에 v1 endpoint들을 모아두는 router가 들어갑니다. 버전업을 하는 경우 `v2`, `v3`...로 네이밍을 할 수 있습니다.

`v1/endpoints` : endpoint 중에서도 관련성 있는 endpoint끼리 묶기 위해서 만든 폴더입니다.

`v1/daos` : Data Access Object. database에 접근하는 객체를 저장해놓은 폴더입니다.

`v1/models` : 이 폴더 안에는 `v1` Endpoints에 대한 data model을 정의하는 파일들이 들어갑니다.

`v1/schemas` : `schema`는 pydantic 모델을 의미합니다. `schemas`로 이름을 지은 이유는 FastAPI가 OpenAPI specification을 기반이고, 이 안의 파일들이 사실상 Swagger 생성부터 엔드포인트의 request body까지 어디에서나 사용하는 OpenAPI schema를 생성하기 때문입니다. 이 폴더 안에는 `v1` Endpoints에 대한 schema를 정의하는 파일들이 들어갑니다.

`consts.py` : 상수를 넣는 파일입니다.

---
## 필요한 API Endpoint

### Users

- [ ] 회원가입
  - [ ] 이메일 인증?
  - [ ] 소셜 로그인?
- [ ] 로그인
- [ ] 프로필 수정
- [ ] 프로필 이미지 변경

### Video

- [ ] 비디오 업로드
- [ ] 비디오 description 수정
- [ ] 비디오 삭제
- [ ] 비디오의 댓글 불러오기
- [ ] 썸네일 이미지 설정 기능

### Comment

- [ ] 댓글 작성 / 수정 / 삭제
### Future

- [ ] SocketIO 및 WebRTC를 이용한 스트리밍?
- [ ] 채팅?


