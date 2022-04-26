export interface TokenResponse {
    access_token: string
    refresh_token: string
}

export interface UserResponse {
    username: string
    email: string
    is_verified: boolean
}

export interface ChatResponse {
    id: number,
    name: string
}

export interface MessageResponse {
    id: number,
    text: string,
    sending_time: string,
    chat: ChatResponse
}
