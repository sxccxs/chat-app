import {RegistrationData, RequestException, Result, User, VResult} from "../models";
import {ACCESS_KEY, api, REFRESH_KEY} from "../http";
import {TokenResponse, UserResponse} from "../http/responses";
import {AxiosResponse} from "axios";
import {ActivateRequest, LoginRequest, RegistrationRequest} from "../http/requests";
import {apiRoutes, routes} from "../resources";

export class UserService {
    public static async Login(email: string, password: string): Promise<VResult<User, RequestException>> {
        try {
            let tokens = (await api.post<TokenResponse, AxiosResponse, LoginRequest>(apiRoutes.login, {
                email: email,
                password: password
            })).data;
            this.SaveTokens(tokens);
            let userResult = await this.GetUser()
            if (userResult.isSuccess) {
                return {isSuccess: true, value: userResult.value}
            }

            return {isSuccess: false, exception: userResult.exception}
        } catch (ex) {
            if (ex instanceof RequestException) {
                return {isSuccess: false, exception: ex}
            }

            throw ex;
        }
    }

    public static async GetUser(): Promise<VResult<User, RequestException>> {
        try {
            let userData = (await api.get<UserResponse>(apiRoutes.getUserData)).data;
            return {isSuccess: true, value: new User(userData.username, userData.email)}
        } catch (ex) {
            if (ex instanceof RequestException) {
                return {isSuccess: false, exception: ex}
            }

            throw ex
        }
    }

    public static async CheckEmail(email: string): Promise<VResult<boolean, RequestException>> {
        try{
            api.post()
        }
    }

    public static async Register(userData: RegistrationData): Promise<Result<RequestException>> {
        try {
            await api.post<null, AxiosResponse, RegistrationRequest>(apiRoutes.registration, {
                user: {
                    username: userData.username,
                    email: userData.email,
                    password: userData.password,
                },
                activation_url: routes.activation,
            })

            return {isSuccess: true};
        } catch (ex) {
            if (ex instanceof RequestException) {
                return {isSuccess: false, exception: ex}
            }

            throw ex
        }
    }

    public static async Activate(uid: string, token: string): Promise<Result<RequestException>> {
        try {
            await api.post<null, AxiosResponse, ActivateRequest>(apiRoutes.activate, {
                uidb64: uid,
                token: token
            })
            return {isSuccess: true}
        } catch (ex) {
            if (ex instanceof RequestException) {
                return {isSuccess: false, exception: ex}
            }

            throw ex
        }
    }

    public static Logout() {
        localStorage.removeItem(ACCESS_KEY)
        localStorage.removeItem(REFRESH_KEY)
    }

    private static SaveTokens(tokens: TokenResponse): void {
        localStorage.setItem(ACCESS_KEY, tokens.access_token)
        localStorage.setItem(REFRESH_KEY, tokens.refresh_token)
    }
}