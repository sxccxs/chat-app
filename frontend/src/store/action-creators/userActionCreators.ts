import {Dispatch} from "react";
import {UserAction} from "../actions";
import {UserActionType} from "../action-types";
import {User} from "../../models";

export const logout = () => {
    return (dispatch: Dispatch<UserAction>) => {
        dispatch({
            type: UserActionType.LOGOUT
        })
    }
}

export const login = (user: User | null) => {
    return (dispatch: Dispatch<UserAction>) => {
        dispatch({
            type: UserActionType.LOGIN,
            payload: user,
        })
    }
}