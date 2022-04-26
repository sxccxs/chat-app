import {Chat} from "../../models";
import {ChatsAction} from "../actions";
import {ChatsActionType} from "../action-types";

const reducer = (state: Chat[] = [], action: ChatsAction): Chat[] => {
    switch (action.type) {
        case ChatsActionType.CREATE:
            return [...state, action.payload]
        case ChatsActionType.CREATE_MANY:
            return [...state, ...action.payloads]
        case ChatsActionType.UPDATE:
            return state.map(c => c.id === action.payload.id ? action.payload : c)
        case ChatsActionType.DELETE:
            return state.filter(c => c.id !== action.payload.id)
        case ChatsActionType.ADD_MESSAGE:
            let chat = state.find(c => c.id === action.payload.chatId)
            if (chat !== undefined) {
                chat.messages.push(action.payload)
                return state.map(c => c.id === chat!.id ? chat! : c)
            }
            return state
        default:
            return state;
    }
}

export default reducer;