import sqlalchemy
from db.db_session import SqlAlchemyBase


class Tasks(SqlAlchemyBase):
    __tablename__ = 'tasks'

    task_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    task_text = sqlalchemy.Column(sqlalchemy.String(1000), nullable=False)
    task_author = sqlalchemy.Column(sqlalchemy.Integer)
    task_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
