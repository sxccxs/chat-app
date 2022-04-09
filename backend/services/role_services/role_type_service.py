from sqlalchemy.orm import Session

from models import models


def get_role_type_by_name(db: Session, name: str) -> models.RoleType:
    return db.query(models.RoleType).filter_by(name=name).first()


def create_role_type(db: Session, name: str) -> None:
    role_type = models.RoleType(name=name)
    db.add(role_type)
    db.commit()
