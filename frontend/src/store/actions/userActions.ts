import {User} from "../../models";
import {UserActionType} from "../action-types";

interface LoginAction {
    type: UserActionType.LOGIN,
    payload: User | null
}

interface LogoutAction {
    type: UserActionType.LOGOUT,
}

export type UserAction = LoginAction | LogoutAction;