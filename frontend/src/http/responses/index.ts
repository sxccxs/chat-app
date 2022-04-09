export interface TokenResponse{
    access_token: string
    refresh_token: string
}

export interface UserResponse{
    username: string
    email: string
}

export interface EmailCheckResponse{
   result: boolean
}