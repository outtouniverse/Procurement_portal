def Trial():
    print("yes! it's working")


    # models/user.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from passlib.hash import bcrypt

from Backend.database import Base  # assuming you have database.py with Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def verify_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.password_hash)

    def set_password(self, password: str):
        self.password_hash = bcrypt.hash(password)


# ========== CRUD Helper Functions ==========

def create_user(db, username: str, email: str, password: str):
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_username(db, username: str):
    return db.query(User).filter(User.username == username).first()
