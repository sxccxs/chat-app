import {Dispatch} from "react";
import {ChatsActionType} from "../action-types";
import {ChatsAction} from "../actions";
import {Chat, Message, MessageCreate} from "../../models";

export const create = (chat: Chat) => {
    return (dispatch: Dispatch<ChatsAction>) => {
        dispatch({
            type: ChatsActionType.CREATE,
            payload: chat
        })
    }
}

export const createMany = (chats: Chat[]) => {
    return (dispatch: Dispatch<ChatsAction>) => {
        dispatch({
            type: ChatsActionType.CREATE_MANY,
            payloads: chats
        })
    }
}

export const update = (chat: Chat) => {
    return (dispatch: Dispatch<ChatsAction>) => {
        dispatch({
            type: ChatsActionType.UPDATE,
            payload: chat
        })
    }
}

export const delete_ = (chat: Chat) => {
    return (dispatch: Dispatch<ChatsAction>) => {
        dispatch({
            type: ChatsActionType.DELETE,
            payload: chat
        })
    }
}

export const addMessage = (payload: Message) => {
    return (dispatch: Dispatch<ChatsAction>) => {
        dispatch({
            type: ChatsActionType.ADD_MESSAGE,
            payload: payload
        })
    }
}

export const sendMessage = (payload: MessageCreate) => {
    return (dispatch: Dispatch<ChatsAction>) => {
        dispatch({
            type: ChatsActionType.SEND_MESSAGE,
            payload: payload
        })
    }
}