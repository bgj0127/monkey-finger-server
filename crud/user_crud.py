from sqlalchemy.orm import Session
from models import User
from schema import UserForm

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def insert_user(new_user: UserForm, db: Session):
    user = User(
        user_id=new_user.user_id,
        user_pw=pwd_context.hash(new_user.user_pw),
    )
    db.add(user)
    db.commit()

    return user.user_id


def get_user(user_id: str, db: Session):
    user = db.query(User).filter(User.user_id == user_id).first()
    return user
