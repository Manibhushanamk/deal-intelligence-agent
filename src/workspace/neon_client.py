import logging
import json
from typing import Dict, Any, Optional
from sqlalchemy import create_engine, Column, String, Float, Text, DateTime, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone
from src.config import config

logger = logging.getLogger("NeonDatabaseClient")
logger.setLevel(logging.INFO)

Base = declarative_base()

class DealRecordModel(Base):
    __tablename__ = "deal_records"

    opportunity_id = Column(String(100), primary_key=True)
    account_id = Column(String(100), nullable=False, index=True)
    deal_name = Column(String(200), nullable=False)
    stage = Column(String(50), nullable=False)
    arr = Column(Float, nullable=False, default=0.0)
    win_probability = Column(Float, nullable=False, default=0.5)
    deal_metadata = Column(JSON, nullable=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class NeonDatabaseClient:
    """
    Client for persisting structured deal state and interaction logs into Neon PostgreSQL database.
    """
    def __init__(self, db_url: Optional[str] = None):
        self.db_url = db_url or config.NEON_DATABASE_URL
        self._engine = None
        self._Session = None
        self._in_memory_records: Dict[str, Dict[str, Any]] = {}

        # Attempt to establish real SQLAlchemy database engine
        try:
            if self.db_url and not "mock" in self.db_url:
                self._engine = create_engine(self.db_url, pool_pre_ping=True)
                Base.metadata.create_all(self._engine)
                self._Session = sessionmaker(bind=self._engine)
                logger.info("[Neon DB] Engine initialized successfully.")
        except Exception as e:
            logger.warning(f"[Neon DB] Connection failed ({e}), using fallback store.")

    def persist_deal_record(self, account_id: str, opportunity_id: str, deal_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Persists structured deal record to Neon PostgreSQL with fallback.
        """
        if self._Session:
            try:
                session = self._Session()
                existing = session.query(DealRecordModel).filter_by(opportunity_id=opportunity_id).first()
                if existing:
                    existing.stage = deal_data.get("stage", existing.stage)
                    existing.arr = deal_data.get("arr", existing.arr)
                    existing.win_probability = deal_data.get("win_probability", existing.win_probability)
                    existing.deal_metadata = deal_data
                    existing.updated_at = datetime.now(timezone.utc)
                else:
                    new_record = DealRecordModel(
                        opportunity_id=opportunity_id,
                        account_id=account_id,
                        deal_name=deal_data.get("deal_name", f"Deal {opportunity_id}"),
                        stage=deal_data.get("stage", "Qualification"),
                        arr=deal_data.get("arr", 0.0),
                        win_probability=deal_data.get("win_probability", 0.5),
                        deal_metadata=deal_data
                    )
                    session.add(new_record)
                session.commit()
                session.close()
                logger.info(f"[Neon DB] Successfully persisted deal {opportunity_id} to PostgreSQL.")
                return {"status": "persisted_to_neon", "account_id": account_id, "opportunity_id": opportunity_id}
            except Exception as e:
                logger.warning(f"[Neon DB] Write failed ({e}), using fallback.")

        self._in_memory_records[opportunity_id] = deal_data
        return {"status": "persisted_to_neon_fallback", "account_id": account_id, "opportunity_id": opportunity_id}
