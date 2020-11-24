import logging

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from checker.db.models import Base, Domain
from checker.utils.singleton import Singleton
from config import DATABASE_CONNECTION_URL


class Database(metaclass=Singleton):
    def __init__(self, connection_url: str = DATABASE_CONNECTION_URL, echo: bool = False):
        self._logger = logging.getLogger('[database]')
        self.engine = create_engine(connection_url, echo=echo)
        Base.metadata.create_all(self.engine)
        self.session = Session(bind=self.engine)

    def save(self, domain: Domain):
        self.session.merge(domain)

    def commit(self):
        try:
            self.session.commit()
        except IntegrityError as e:
            self._logger.warning(e)
            self.session.rollback()
        except Exception as e:
            self.session.rollback()
            raise e
