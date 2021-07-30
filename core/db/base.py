from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.orm import Session
from core.db.conn import db


class BaseMixin:
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    created_at = Column(DateTime, nullable=False, default=func.utc_timestamp())
    updated_at = Column(
        DateTime,
        nullable=False,
        default=func.utc_timestamp(),
        onupdate=func.utc_timestamp(),
    )

    def __init__(self):
        # Query
        self._q = None
        # Session
        self._session = None
        # ?
        self.served = None

    # __table__은 declarative_base 의 리턴값으로 나오는 class로 부터 상속받은 값이다.
    # https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/table_config.html#using-a-hybrid-approach-with-table
    def all_columns(self):
        return [
            c
            for c in self.__table__.columns
            if c.primary_key is False and c.name != "created_at"
        ]

    @classmethod
    def create(cls, session: Session, autocommit: bool = False, **kwargs):
        """
        테이블 데이터 적재 전용 함수
        """
        obj = cls()
        for col in obj.all_columns():
            col_name = col.name
            if col_name in kwargs:
                setattr(obj, col_name, kwargs.get(col_name))

        session.add(obj)
        session.flush()  # autoflush=True로 했는데 필요할까?
        if autocommit:
            session.commit()
        return obj

    @classmethod
    def get(cls, session: Session = None, **kwargs):
        """
        Row를 얻는 함수
        """
        one_session = next(db.session()) if not session else session
        query = one_session.query(cls)
        for key, val in kwargs.items():
            col = getattr(cls, key)
            query = query.filter(col == val)

        if query.count() > 1:
            raise Exception(
                "Only one row is supposed to be returned, but got more than one."
            )

        result = query.first()
        if not session:
            one_session.close()
        return result

    @classmethod
    def filter(cls, session: Session = None, **kwargs):
        """
        필터링한 Rows를 리턴한다.?
        """
        cond = []
        # id__gt=3은 id가 3보다 큰 조건 (id > 3)
        # id__gte=3은 id가 3보다 크거나 같은 조건 (id >= 3)
        # id__lt=3은 id가 3보다 작은 조건 (id < 3)
        # id__lte=3은 id가 3보다 작거나 같은 조건 (id <= 3)
        # id__in=[1,2,3]은 id가 1 or 2 or 3인 조건
        for key, val in kwargs.items():
            key = key.split("__")
            if len(key) > 2:
                raise Exception(" No 2 more dunders")
            col = getattr(cls, key[0])
            if len(key) == 1:
                cond.append((col == val))
            elif len(key) == 2 and key[1] == "gt":
                cond.append((col > val))
            elif len(key) == 2 and key[1] == "gte":
                cond.append((col >= val))
            elif len(key) == 2 and key[1] == "lt":
                cond.append((col < val))
            elif len(key) == 2 and key[1] == "lte":
                cond.append((col <= val))
            else:
                cond.append((col._in_(val)))
        obj = cls()
        if session:
            obj._session = session
            obj.served = True
        else:
            obj._session = next(db.session())
            obj.served = False
        query = obj._session.query(cls)
        query = query.filter(*cond)
        obj._q = query
        return obj

    @classmethod
    def cls_attr(cls, col_name=None):
        if col_name:
            col = getattr(cls, col_name)
            return col
        else:
            return cls

    def order_by(self, *args: str):
        for a in args:
            if a.startswith("-"):
                col_name = a[1:]
                is_asc = False
            else:
                col_name = a
                is_asc = True
            col = self.cls_attr(col_name)
            self._q = (
                self._q.order_by(col.asc()) if is_asc else self._q.order_by(col.desc())
            )

    def update(self, autocommit: bool = False, **kwargs):
        qs = self._q.update(kwargs)
        ret = None

        self._session.flush()
        if qs > 0:
            ret = self._q.first()
        if autocommit:
            self._session.commit()
        return ret

    def first(self):
        result = self._q.first()
        self.close()
        return result

    def delete(self, autocommit: bool = False):
        self._q.delete()
        if autocommit:
            self._session.commit()

    def all(self):
        result = self._q.all()
        self.close()
        return result

    def count(self):
        result = self._q.count()
        self.close()
        return result

    def close(self):
        if not self.served:
            self._session.close()
        else:
            self._session.flush()
