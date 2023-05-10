#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """add a new user to database"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs: dict) -> User:
        """filter user based on args"""
        for k, v in kwargs.items():
            try:
                val = 'User.' + k
                return self._session.query(User).filter(eval(val) == v).one()
            except Exception:
                if NoResultFound:
                    raise NoResultFound
                else:
                    raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs: dict) -> None:
        """update existing user data"""
        user = self.find_user_by(id=user_id)
        for k, v in kwargs.items():
            try:
                user.__dict__[k]
            except Exception:
                raise ValueError
            else:
                user.__dict__[k] = v
        self._session.commit()
