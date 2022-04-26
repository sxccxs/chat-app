import {RequestException, Result, VResult} from "../models";

export * from './FormValidationService'
export * from './UserService';

type ResultReturn<T = {}> = Result<RequestException> | VResult<T, RequestException>

export const httpFuncWrapper = async <T extends ResultReturn>(func: () => Promise<T>): Promise<T> => {
    try {
        return await func()
    } catch (ex) {
        if (ex instanceof RequestException) {
            return {isSuccess: false, exception: ex} as T
        }

        throw ex;
    }
}