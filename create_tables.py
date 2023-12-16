from sqlalchemy import MetaData

from core.configs import settings
from core.database import engine

def create_tables() -> None:
    import models.__all__models
    
    with engine.begin() as conn:
        settings.DBBaseModel.metadata.create_all(conn)
        
if __name__ == "__main__":
    create_tables()