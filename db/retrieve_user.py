from fastapi import HTTPException
from sqlalchemy.orm.session import Session
from model.models import User


def get_user_by_username(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    # Handle any exceptions
    if not user:
        raise HTTPException(status_code=404, detail=f'User with username: {username} not found!')
    return user