import sqlalchemy
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative

from data.config import sql_types

SqlAlchemyBase = sqlalchemy.ext.declarative.declarative_base()

__factory = None


def global_init(sql_type: str):
    global __factory

    if __factory:
        return

    engine = sqlalchemy.create_engine(sql_types[sql_type])
    __factory = sqlalchemy.orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
