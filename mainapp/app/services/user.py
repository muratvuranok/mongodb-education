from sqlalchemy.orm import Session
from models.user import UserModel
from schemas.user import UserRequest, UserResponse
from passlib.context import CryptContext  # password hashing
from extensions.stringExtensions import StringExtensions

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_user(db: Session, user: UserRequest):  # -> UserResponse:
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(
        username=StringExtensions.to_username(user.username),
        email=user.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # return UserResponse(db_user.username, db_user.email)
    return db_user


def update_refres_token(db: Session, username: str, refresh_token: str):
    user = get_user_by_username(db, username)
    if user:
        user.refresh_token = refresh_token
        db.commit()
        db.refresh(user)
        return user
    return None


def get_user_by_username(db: Session, username: str):  # -> UserModel:
    return (
        db.query(UserModel)
        .filter(UserModel.username == StringExtensions.to_username(username))
        .first()
    )


def get_user_by_refrehtoken(db: Session, refresh_token: str):
    return db.query(UserModel).filter(UserModel.refresh_token == refresh_token).first()
