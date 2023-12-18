from datetime import datetime

from core.database import Session
from models.__all__models import LogModel
from schemas.log_schemas import LogSchema


class Logger:
    def save_log(self, full_log: str, log_level: str, issued_from: str):
        log = LogModel(
            full_log=full_log,
            log_level=log_level,
            issued_from=issued_from,
            issued_at=datetime.now(),
        )
        with Session() as session:
            try:
                session.execute(
                    "CALL sp_setLog(:param_full_log, :param_log_level, :param_issued_from, :param_issued_at)",
                    {
                        "param_full_log": log.full_log,
                        "param_log_level": log.log_level,
                        "param_issued_from": log.issued_from,
                        "param_issued_at": log.issued_at,
                    },
                )
                session.commit()
            except Exception as ex:
                session.rollback()
                print("***** Error while saving log *****")
                print(f"***** {ex} *****")
            finally:
                session.close()
                
logger = Logger()
