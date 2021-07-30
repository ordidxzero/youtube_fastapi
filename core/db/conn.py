import logging
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

logging.basicConfig(level=logging.INFO)

# 딱 한 곳에서만 DB Session Pool을 유지하기 위해서 싱글톤을 사용해야한다.
class SQLAlchemy:
    # _engine, _session 초기화
    def __init__(self, app: FastAPI = None, **kwargs):
        self._engine: Engine = None
        self._session: sessionmaker = None
        if app is not None:
            self.init_app(app=app, **kwargs)

    # _engine, _session 생성
    def init_app(self, app: FastAPI, **kwargs):
        """
        DB 초기화 함수
        """
        database_url = kwargs.get("DB_URL")
        pool_recycle = kwargs.get("DB_POOL_RECYCLE", 900)
        echo = kwargs.get("DB_ECHO", True)
        # DB Engine
        # echo = DB Query가 찍힌다.
        # pool_recycle = connection을 재사용할 시간? (주어진 초(seconds) 이후에 connection을 재사용한다.)
        # pool_pre_ping = True면 각 체크아웃시 connection을 테스트하는 connection pool "pre-ping" 기능을 활성화한다.
        self._engine = create_engine(
            database_url, echo=echo, pool_recycle=pool_recycle, pool_pre_ping=True
        )
        # Session
        # autocommit = commit이란 모든 작업을 정상적으로 처리하겠다고 확정하는 명령어다. 실수를 방지하기 위해서 끄는 것이 좋다.
        # autoflush = 트랜잭션을 수행하고 그것을 기억하도록하는 옵션. commit이 실행되지않으면 disk에는 저장되지 않는다.
        self._session = sessionmaker(
            autocommit=False, autoflush=True, bind=self._engine
        )

        # startup이벤트(FastAPI 앱이 시작할 때 발생하는 이벤트)가 발생했을 때 실행될 함수
        # _engine을 연결하고 log를 남긴다.
        @app.on_event("startup")
        def startup():
            self._engine.connect()
            logging.info("DB connected.")

        # shutdown이벤트(FastAPI 앱이 시작할 때 발생하는 이벤트)가 발생했을 때 실행될 함수
        # 모든 session과 engine을 닫고 log를 남긴다.
        @app.on_event("shutdown")
        def shutdown():
            self._session.close_all()
            self._engine.dispose()
            logging.info("DB disconnected.")

    def get_db(self):
        """
        요청마다 DB session을 유지하는 함수
        """
        if self._session is None:
            raise Exception("must be called 'init_app'")
        db_session = None
        try:
            db_session = self._session()
            yield db_session
        except:
            db_session.close()

    @property
    def session(self):
        return self.get_db

    @property
    def engine(self):
        return self._engine


db = SQLAlchemy()
# 상속 클래스들을 자동으로 인지하고 알아서 매핑해주는 역할
Base = declarative_base()
