import {
    AccountEditData,
    PasswordChangeData,
    RegistrationData,
    RequestException,
    Result,
    User,
    VResult
} from "../models";
import {ACCESS_KEY, api, REFRESH_KEY} from "../http";
import {TokenResponse, UserResponse} from "../http/responses";
import {AxiosResponse} from "axios";
import {
    AccountEditRequest,
    ActivateRequest, ChangePasswordRequest, ConfirmResetPasswordRequest,
    EmailCheckRequest,
    LoginRequest,
    RegistrationRequest, ResetPasswordRequest
} from "../http/requests";
import {apiRoutes, routes} from "../resources";
import {httpFuncWrapper} from "./index";

export class UserService {
    public static async Login(email: string, password: string): Promise<VResult<User, RequestException>> {
        return await httpFuncWrapper(async () => {
            let tokens = (await api.post<TokenResponse, AxiosResponse, LoginRequest>(apiRoutes.login, {
                email: email,
                password: password
            })).data as TokenResponse;
            this.SaveTokens(tokens);
            let userResult = await this.GetUser()
            if (userResult.isSuccess) {
                return {isSuccess: true, value: userResult.value}
            }

            return {isSuccess: false, exception: userResult.exception}
        })
    }

    public static async GetUser(): Promise<VResult<User, RequestException>> {
        return await httpFuncWrapper(async () => {
            let userData = (await api.get<UserResponse>(apiRoutes.getUserData)).data;
            return {isSuccess: true, value: new User(userData.username, userData.email, userData.is_verified)}
        })
    }

    public static async EmailExists(email: string): Promise<Result<RequestException>> {
        return await httpFuncWrapper(async () => {
            await api.post<null, AxiosResponse, EmailCheckRequest>(apiRoutes.checkEmail, {
                email: email
            })

            return {isSuccess: true}

        })
    }

    public static async Register(userData: RegistrationData): Promise<Result<RequestException>> {
        return await httpFuncWrapper(async () => {
            await api.post<null, AxiosResponse, RegistrationRequest>(apiRoutes.registration, {
                user: {
                    username: userData.username,
                    email: userData.email,
                    password: userData.password,
                },
                activation_url: routes.activation,
            })

            return {isSuccess: true};

        })
    }

    public static async VerifyEmail(uid: string, token: string): Promise<Result<RequestException>> {
        return await httpFuncWrapper(async () => {
            await api.post<null, AxiosResponse, ActivateRequest>(apiRoutes.activate, {
                uidb64: uid,
                token: token
            })
            return {isSuccess: true}

        })
    }

    public static async EditAccountData(data: AccountEditData): Promise<VResult<User, RequestException>> {
        return await httpFuncWrapper(async () => {
            let requestData: AccountEditRequest = {user_data: {username: ""}};
            if (data.username !== undefined && data.email === undefined) {
                requestData = {user_data: {username: data.username}}
            } else if (data.username === undefined && data.email !== undefined) {
                requestData = {user_data: {email: data.email}, activation_url: routes.activation}
            } else if (data.username !== undefined && data.email !== undefined) {
                requestData = {
                    user_data: {username: data.username, email: data.email},
                    activation_url: routes.activation
                }
            }

            let user = (await api.put<UserResponse, AxiosResponse, AccountEditRequest>(apiRoutes.editAccountData,
                requestData)).data as UserResponse;
            return {isSuccess: true, value: new User(user.username, user.email, user.is_verified)}
        })
    }

    public static async ChangePassword(passwords: PasswordChangeData): Promise<Result<RequestException>> {
        return await httpFuncWrapper(async () => {
            let tokensData = (await api.put<TokenResponse, AxiosResponse, ChangePasswordRequest>(apiRoutes.changePassword, {
                old_password: passwords.oldPassword,
                new_password: passwords.newPassword,
            })).data as TokenResponse
            this.SaveTokens(tokensData)
            return {isSuccess: true}
        })
    }

    public static async RequestResetPassword(email: string): Promise<Result<RequestException>> {
        return await httpFuncWrapper(async () => {
            await api.post<null, AxiosResponse, ResetPasswordRequest>(apiRoutes.requestResetPassword, {
                email: email,
                reset_url: routes.passwordReset
            })

            return {isSuccess: true}
        })
    }

    public static async ResetPasswordConfirm(uid: string, token: string, newPassword: string): Promise<Result<RequestException>> {
        return await httpFuncWrapper(async () => {
            await api.post<null, AxiosResponse, ConfirmResetPasswordRequest>(apiRoutes.resetPasswordConfirm, {
                uidb64: uid,
                token: token,
                new_password: newPassword
            })
            return {isSuccess: true}
        })
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