import yagmail
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config
from controllers.routers import auth_router, account_router
from models import models
from models.db import engine
from services import setup_service

models.Base.metadata.create_all(bind=engine)
setup_service.setup()
yagmail.register(config.EMAIL_USER, config.EMAIL_PASSWORD)

origins = [
    "http://localhost:3000",
    "http://localhost:3000/*"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(account_router)
