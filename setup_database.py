from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from database import *

from dotenv import load_dotenv
from os import getenv

load_dotenv()

DB_DIALECT_DRIVER = getenv("DB_DIALECT_DRIVER")
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_NAME = getenv("DB_NAME")

TEMP = "postgres"

def create_database(db_uri) -> None:
    engine = create_engine(db_uri)
    try:
        with engine.connect() as connection:
            connection.execute(text(f"CREATE DATABASE {DB_NAME}"))
            print(f"Database {DB_NAME} created successfully.")

    except OperationalError as e:
        if "already exists" in str(e):
            print(f"Database {DB_NAME} already exists.")
        
        else:
            print(f"An error occurred: {e}")
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        engine.dispose()

def create_columns(db_uri) -> None:
    engine = create_engine(db_uri)

    try:
        base.metadata.create_all(engine)
        print("Tables created successfully.")

    except Exception as e:
        print(f"An error occurred while creating columns: {e}")

    finally:
        engine.dispose()

if __name__ == "__main__":
    create_database(f"{DB_DIALECT_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{TEMP}")
    create_columns(f"{DB_DIALECT_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")