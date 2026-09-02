from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class Prediction(Base):

    __tablename__ = "predictions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    match_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    predicted_home_score = Column(
        Integer,
        nullable=False
    )

    predicted_away_score = Column(
        Integer,
        nullable=False
    )

    predicted_result = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    user = relationship(
        "User",
        back_populates="predictions"
    )