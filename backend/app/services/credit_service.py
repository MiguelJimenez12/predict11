from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.user import User

INITIAL_CREDITS = 20
DAILY_CREDITS = 3
MAX_FREE_CREDITS = 20


def refreshed_balance(balance: int, last_refresh: datetime | None, now: datetime) -> tuple[int, datetime]:
    if last_refresh is None:
        return balance, now
    if last_refresh.tzinfo is None:
        last_refresh = last_refresh.replace(tzinfo=timezone.utc)
    elapsed_days = (now.date() - last_refresh.astimezone(timezone.utc).date()).days
    if elapsed_days <= 0:
        return balance, last_refresh
    return min(MAX_FREE_CREDITS, balance + elapsed_days * DAILY_CREDITS), now


def consume_prediction_credit(db: Session, user_id: int, now: datetime | None = None) -> int | None:
    """Atomically validate, refresh and consume credits on the backend."""
    now = now or datetime.now(timezone.utc)
    user = db.query(User).filter(User.id == user_id).with_for_update().one_or_none()
    if user is None:
        raise ValueError("Usuario no encontrado.")
    if user.subscription_type == "premium" and user.subscription_status == "active":
        return None

    user.prediction_credits, user.last_credit_refresh = refreshed_balance(
        user.prediction_credits,
        user.last_credit_refresh,
        now,
    )
    if user.prediction_credits <= 0:
        raise ValueError("No tienes creditos disponibles.")
    user.prediction_credits -= 1
    db.commit()
    return user.prediction_credits
