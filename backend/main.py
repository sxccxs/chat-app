import logging

import socketio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config
from controllers.messages import MessagesNamespace
from controllers.routers import auth_router, account_router, chats_router
from models.db import database
from services import setup_service
from sockets import sio


app = FastAPI()
socketio_app = socketio.ASGIApp(sio, app)
app.state.database = database


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()
    await setup_service.setup()
    logging.info("App started up")


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()
    logging.info("App shuted down")


app.add_middleware(
    CORSMiddleware,
    allow_origins=config.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(account_router)
app.include_router(chats_router)
sio.register_namespace(MessagesNamespace("/messages"))

if __name__ == "__main__":
    uvicorn.run("main:socketio_app", reload=True)
