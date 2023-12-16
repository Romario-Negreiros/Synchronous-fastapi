from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session as SyncSession
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.mock import MockConnection
from core.configs import settings

engine: MockConnection = create_engine(settings.DB_URL)
engine

Session: SyncSession = sessionmaker(
    autocommit       = False,
    autoflush        = False,
    expire_on_commit = False,
    class_           = SyncSession,
    bind             = engine
)
