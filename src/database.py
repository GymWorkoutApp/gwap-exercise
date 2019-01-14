from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session

from src.settings import DatabaseConfig

master_engine = create_engine(DatabaseConfig.get_uri())
read_replica_engine = create_engine(DatabaseConfig.get_uri())

db = SQLAlchemy()


@contextmanager
def master_async_session() -> scoped_session:
    session = db.create_scoped_session(
        options=dict(bind=master_engine, binds={})
    )
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()


@contextmanager
def read_replica_async_session() -> scoped_session:
    session = db.create_scoped_session(
        options=dict(bind=read_replica_engine, binds={})
    )
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()
