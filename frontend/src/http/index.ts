import axios, {AxiosRequestConfig, AxiosResponse} from "axios";
import {TokenResponse} from "./responses";
import {RefreshRequest} from "./requests";
import {RequestException} from "../models";

export const API_URL = "http://127.0.0.1:8000"
export const ACCESS_KEY = "access"
export const REFRESH_KEY = "refresh"


export const api = axios.create({
    withCredentials: true,
    baseURL: API_URL,
})

api.interceptors.request.use((config) => {
    config.headers = {
        "Authorization": `Bearer ${localStorage.getItem(ACCESS_KEY)}`,
    }
    return config;
})

api.interceptors.response.use(
    (response) => response,
    async ({response}: { response: AxiosResponse<string> }): Promise<RequestException> => {
        const originalConfig = response.config as AxiosRequestConfig & { _isRetry?: boolean };
        if (response.request.status === 401 && originalConfig && !originalConfig?._isRetry) {
            originalConfig._isRetry = true;
            try {
                const response = await api.post<TokenResponse, AxiosResponse, RefreshRequest>(`/auth/refresh`, {
                    refresh_token: localStorage.getItem(REFRESH_KEY)
                })
                localStorage.setItem(ACCESS_KEY, response.data.access_token)
                localStorage.setItem(REFRESH_KEY, response.data.refresh_token)
                return api.request(originalConfig)
            } catch {
                localStorage.removeItem(ACCESS_KEY)
                localStorage.removeItem(REFRESH_KEY)
                return Promise.reject(new RequestException(response.status, response.data))
            }
        }

        return Promise.reject(new RequestException(response.status, response.data))
    }
)