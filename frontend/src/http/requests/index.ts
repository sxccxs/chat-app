import {AccountEditData} from "../../models";

export interface RefreshRequest {
    refresh_token: string | null
}

export interface LoginRequest {
    email: string
    password: string
}

interface RegistrationData {
    username: string
    email: string
    password: string
}

export interface RegistrationRequest {
    user: RegistrationData,
    activation_url: string
}

export interface ActivateRequest {
    uidb64: string,
    token: string
}

export interface EmailCheckRequest {
    email: string
}

export type AccountEditRequest = {
    user_data: {
        username: string
    }
} | {
    user_data: {
        username: string,
        email: string
    },
    activation_url: string,
} | {
    user_data: {
        email: string
    },
    activation_url: string,
}

export interface ChangePasswordRequest {
    old_password: string,
    new_password: string,
}

export interface ResetPasswordRequest {
    email: string,
    reset_url: string,
}

export interface ConfirmResetPasswordRequest {
    uidb64: string,
    token: string,
    new_password: string,
}

export interface ChatCreateRequest {
    name: string
}

export interface ChatEditRequest {
    id: number
    name: string
}

export interface ChatDeleteRequest {
    chat_id: number
}