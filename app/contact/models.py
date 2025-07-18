from sqlalchemy import Column, DateTime, Integer, String, func

from app.db.database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    phone = Column(String(50))
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
