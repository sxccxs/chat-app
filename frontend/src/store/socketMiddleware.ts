import {bindActionCreators, Middleware} from 'redux'
import {ACCESS_KEY} from "../http";
import {apiRoutes} from "../resources";
import {ChatsActionType, UserActionType} from "./action-types";
import {ChatResponse, MessageResponse} from "../http/responses";
import {Chat, Message, MessageCreate} from "../models";
import {chatsActionCreators} from "./action-creators"
import {io, Socket} from "socket.io-client";


const socketMiddleware: Middleware = store => {
    let socket: Socket

    return next => action => {
        if (!socket) {
            socket = io(`http://127.0.0.1:8000${apiRoutes.messages}`, {
                auth: {
                    token: localStorage.getItem(ACCESS_KEY),
                }
            })
            socket.on("chats_get", (responseData: string) => {
                let data: ChatResponse[] = JSON.parse(responseData);
                let chats = data.map(c => new Chat(c.id, c.name))
                const {createMany} = bindActionCreators(chatsActionCreators, store.dispatch)
                createMany(chats)
                chats.forEach(c => socket.emit("messages_get", c.id))
            })
            socket.on("messages_get", (data: string[]) => {
                let messages: MessageResponse[] = data.map((m: string) => JSON.parse((m)))
                const {addMessage} = bindActionCreators(chatsActionCreators, store.dispatch)
                messages.forEach(m => addMessage(new Message(m.id, m.text, m.chat.id, m.sending_time)))
            })
            socket.on("connect_error", (err) => {
                console.log(err)
            })
            socket.on("message", (responseData: string) => {
                let data: MessageResponse = JSON.parse(responseData);
                let message = new Message(data.id, data.text, data.chat.id, data.sending_time)
                const {addMessage} = bindActionCreators(chatsActionCreators, store.dispatch)
                addMessage(message)
            })
        }

        if (ChatsActionType.SEND_MESSAGE.match(action.type) && socket) {
            socket.emit("message", JSON.stringify(action.payload))
        }
        if (UserActionType.LOGOUT.match(action.type) && socket){
            socket.disconnect()
        }

        next(action)
    }
}

export default socketMiddleware;