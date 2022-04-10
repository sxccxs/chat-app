from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from docs import docs
from models.db import session_maker
from models.models import User
from schemas import model_schemas as schemas

from services.user_services import auth_service

router = APIRouter(
    prefix="/me",
    tags=["accounts"],
)


@router.get("", response_model=schemas.UserOut, responses=docs.get("me"))
async def get_account_data(user: User = Depends(auth_service.authenticate)):
    return user


@router.get("/chats", response_model=list[schemas.ChatOut])
async def get_chats(user: User = Depends(auth_service.authenticate)):
    with session_maker() as session:
        session: Session
        user = session.merge(user)
        session.refresh(user)
        return user.chats
