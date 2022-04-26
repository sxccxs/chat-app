import json
import logging

import socketio
from pydantic import ValidationError

from models.models import User
from schemas.model_schemas import MessageOut, MessageCreate, ChatOut
from services import message_service
from services.chat_services import chat_service
from services.user_services.auth_service import authenticate_socket
from sockets import sio

logger = logging.getLogger()


class MessagesNamespace(socketio.AsyncNamespace):
    user: User

    async def on_connect(self, sid: str, environ: dict[str, str], auth: dict[str, str]):
        self.user = await authenticate_socket(auth)
        chats = await chat_service.get_user_chats(self.user)
        for chat in chats:
            sio.enter_room(sid, str(chat.id), self.namespace)

        data = json.dumps(list(map(lambda c: ChatOut.from_orm(c).dict(), chats)))
        await sio.emit("chats_get", data, to=sid, namespace=self.namespace)
        logger.debug("User with id=%d connected successfully", self.user.id)

    def on_disconnect(self):
        logger.debug("User with id=%d has disconnected", self.user.id)

    async def on_messages_get(self, sid, chat_id: int):
        messages_result = await message_service.get_messages_for_chat_and_user(chat_id, self.user)
        if not messages_result.is_success:
            return
        messages = messages_result.value
        data = list(map(lambda m: MessageOut.from_orm(m).json(), messages))
        await sio.emit("messages_get", data, to=sid, namespace=self.namespace)

    async def on_message(self, sid, data: str):
        try:
            msg = MessageCreate.parse_raw(data)
            msg_result = await message_service.create_message(msg, self.user)
            if not msg_result.is_success:
                logger.warning(msg_result.message)
                return

            msg = msg_result.value
            return_msg = MessageOut.from_orm(msg)
            await sio.emit("message", return_msg.json(), room=str(msg.chat.id), namespace=self.namespace)
        except ValidationError as ex:
            logger.warning(ex)
            return
