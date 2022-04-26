import {Chat, Message, MessageCreate, User} from "../../models";
import {ChatsActionType, UserActionType} from "../action-types";

interface LoginAction {
    type: UserActionType.LOGIN,
    payload: User | null
}

interface LogoutAction {
    type: UserActionType.LOGOUT,
}

export type UserAction = LoginAction | LogoutAction;

interface CreateChatAction {
    type: ChatsActionType.CREATE
    payload: Chat
}

interface CreateManyChatsAction {
    type: ChatsActionType.CREATE_MANY,
    payloads: Chat[]
}

interface UpdateChatAction {
    type: ChatsActionType.UPDATE,
    payload: Chat
}

interface DeleteChatAction {
    type: ChatsActionType.DELETE
    payload: Chat
}

interface AddMessageAction {
    type: ChatsActionType.ADD_MESSAGE,
    payload: Message
}

interface SendMessageAction {
    type: ChatsActionType.SEND_MESSAGE
    payload: MessageCreate
}

export type ChatsAction =
    CreateChatAction
    | CreateManyChatsAction
    | UpdateChatAction
    | DeleteChatAction
    | AddMessageAction
    | SendMessageAction
