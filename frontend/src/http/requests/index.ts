export interface RefreshRequest {
    refresh_token: string | null
}

export interface LoginRequest {
    email: string
    password: string
}

interface RegistrationData{
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

export interface EmailCheckRequest{
    email: string
}