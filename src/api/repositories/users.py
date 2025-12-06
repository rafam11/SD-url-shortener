from sqlalchemy.orm import Session

from src.db.models.users import Users

class UsersRepository:
    
    @staticmethod
    def create(db: Session, user: Users) -> Users:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
