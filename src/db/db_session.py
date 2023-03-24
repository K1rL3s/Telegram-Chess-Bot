from pathlib import Path

import sqlalchemy
from loguru import logger
from sqlalchemy.orm import Session, sessionmaker
import sqlalchemy.ext.declarative as dec


SqlAlchemyBase = dec.declarative_base()

__factory: sessionmaker | None = None


def global_init(db_file: str | Path):
    global __factory

    if __factory:
        return

    if isinstance(db_file, str):
        db_file = db_file.strip()

    if not db_file:
        raise RuntimeError("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file}?check_same_thread=False'
    logger.info(f'Подключение к базе данных "{conn_str}"')

    engine = sqlalchemy.create_engine(conn_str, echo=False)
    __factory = sessionmaker(bind=engine)

    from src.db import __all_models  # noqa

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    if not __factory:
        raise RuntimeError("Брат, а кто global_init вызывать будет?")
    return __factory()
