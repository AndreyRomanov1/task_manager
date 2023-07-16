import sqlalchemy
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative

SqlAlchemyBase = sqlalchemy.ext.declarative.declarative_base()

__factory = None


def global_init(username: str, password: str, host: str, database_name: str):
    global __factory

    if __factory:
        return

    engine = sqlalchemy.create_engine(
        f"mysql+pymysql://{username}:{password}@{host}/{database_name}")
    __factory = sqlalchemy.orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
