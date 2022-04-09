from sqlalchemy.orm import Session

from database.models import Users


def get_users(db: Session, skip: int = 0, limit: int = 100) -> Users:
    return db.query(Users).order_by(Users.id.asc()).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int) -> Users:
    return db.query(Users).filter_by(id=user_id).first()
