import {UserAction} from "../actions";
import {UserActionType} from "../action-types";
import {User} from "../../models";

const reducer = (state: User | null = null, action: UserAction) => {
    switch (action.type) {
        case UserActionType.LOGIN:
            return action.payload
        case UserActionType.LOGOUT:
            return null
        default:
            return state;
    }
}

export default reducer;