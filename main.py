from db import db_session
import config
from db.tasks import Tasks
from datetime import datetime


def create_task(massage: str):
    from re import fullmatch
    templ_1 = r'\d\d.\d\d.\d\d\s\d\d.\d\d\s[\S\s]*'
    templ_2 = r'\d\d.\d\d.\d\d\s[\S\s]*'
    templ_3 = r'\d\d.\d\d\s[\S\s]*'
    print(fullmatch(templ_1, massage))
    print(fullmatch(templ_2, massage))
    print(fullmatch(templ_3, massage))
    print()


# create_task("11.09.23 11.00 qq ")
# create_task("11.09.23 w qd wdq dwf w12.,<рцывц423 ?")
# create_task("11.09 w qd wdq dwf w12.,<рцывц423 ?")

def main():
    db_session.global_init(
        username=config.USERNAME,
        password=config.PASSWORD,
        host=config.HOST,
        database_name=config.DATABASE_NAME
    )
    # t1 = Tasks(
    #     task_text="1 дело",
    #     task_date=datetime(year=2023, month=7, day=20, hour=12, minute=0)
    # )

    # active_session = db_session.create_session()
    # active_session.add(t1)
    # active_session.commit()

    # active_session = db_session.create_session()
    # r = active_session.query(Tasks).filter(Tasks.task_date >= datetime(year=2020, month=1, day=1))
    # print(r.count())


if __name__ == "__main__":
    main()
