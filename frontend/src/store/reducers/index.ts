import {combineReducers} from "redux";
import userReducer from "./userReducer";
import chatsReducer from "./chatsReducer";

const reducers = combineReducers({
    user: userReducer,
    chats: chatsReducer,
})

export default reducers


export type State = ReturnType<typeof reducers>