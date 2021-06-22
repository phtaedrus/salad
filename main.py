import csv
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy import Column, Integer, String, schema
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Date, Text, Enum

pd.set_option('display.max_rows', 500)
FILE = "challenge_dataset.csv"

# sqlAlchemy declarative config
Base = declarative_base()
engine = create_engine('sqlite:///sweetgreen_db', echo=False)


def get_df(file: csv) -> pd.DataFrame():
    with open(FILE) as f:
        df = pd.read_csv(file)
    return df


def transform_df(df):
    # TODO format all of the columns

    df['created_at'] = pd.to_datetime(df.created_at)
    df['birth_date'] = pd.to_datetime(df.birth_date)
    df['age_at_creation'] = round((df['created_at'] - df['birth_date']).dt.days / 365, 1)

    return df


def validate_data(df):
    is_NaN = df[df.isna().any(axis=1)]
    # df['Passed2'] = df['status'].map(lambda x: x.is_integer())
    # TODO with a better rested brain check the logic here, implement and submit.
    df['Passed'] = (df['status'] == 'active') & (df['first_name'] is not np.NaN) & (df['age_at_creation'] >= 18)
    print(df)
    print(is_NaN)
    print(df)
    return df

# TODO create logic to check birthdate against when it was created.
def bday_verify(df):
    df_test = df
    print(df_test)


class PostMetricsAndComments(Base):
    __tablename__ = 'users_new'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    phone = Column(Integer, )
    status = Column(Enum("active", "cancelled"), nullable=False)
    birth_date = Column(Date, nullable=False)
    created_at = Column(Date, nullable=False)


try:
    Base.metadata.create_all(engine)
    print('Database Schema Instantiated')
except sqlalchemy.except_.DatabaseError as db_error:
    print(db_error)


def load_to_sql(df):
    """
    Loads modified pd.Dataframe() objects to sql database.
    args:
    -self, dfs: [pd.Dataframe]
    output:
    Log message
    """
    print(f"Table {df} successfully loaded to SQL DB")

    return


df = validate_data(transform_df(get_df(FILE)))
df.to_sql('users_new', if_exists='replace')
