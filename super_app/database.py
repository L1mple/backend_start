from sqlalchemy import create_engine


SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:1234@db:5432/cars_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

