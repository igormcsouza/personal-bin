from typing import Optional
from os import path

from sqlmodel import Field, SQLModel, create_engine, Session, select


class DataModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: str
    today: float
    five_days: float
    first_day: float
    one_month: float


db_instance = f"{path.expanduser('~')}/bin/databases/findDollarToday.db"
engine = create_engine(f"sqlite:///{db_instance}", echo=False)


def create_tables():
    if not path.isfile(db_instance):
        SQLModel.metadata.create_all(engine)


def insert_one(data: DataModel):
    with Session(engine) as session:
        session.add(data)
        session.commit()


def get_last():
    with Session(engine) as session:
        statement = select(DataModel)
        results: list[DataModel] = session.exec(statement)
        
        timestamp = results[-1].timestamp
        today_rate = results[-1].today
        five_days_ago_diff = results[-1].five_days
        first_day_diff = results[-1].first_day
        one_month_ago_diff = results[-1].one_month

        return timestamp, today_rate, five_days_ago_diff, first_day_diff, one_month_ago_diff

