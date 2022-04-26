import {Chat, ChatEditPayload, Message, RequestException, Result, User, VResult} from "../models";
import {api} from "../http";
import {apiRoutes} from "../resources";
import {ChatResponse, MessageResponse, UserResponse} from "../http/responses";
import {httpFuncWrapper} from "./index";
import {AxiosResponse} from "axios";
import {ChatCreateRequest, ChatDeleteRequest, ChatEditRequest} from "../http/requests";

export class ChatsService {
    public static async GetChatsForUser(): Promise<VResult<Chat[], RequestException>> {
        return await httpFuncWrapper(async () => {
            let chats = (await api.get<ChatResponse[]>(apiRoutes.getChats))
                .data
                .map(cr => new Chat(cr.id, cr.name))
            let userResults = await Promise.all(chats.map(c => this.GetUsersForChat(c.id)))
            let messageResults = await Promise.all(chats.map(c => this.GetMessagesForChat(c.id)))
            for (let i = 0; i < chats.length; i++) {
                let ur = userResults[i]
                let mr = messageResults[i]
                if (ur.isSuccess) {
                    chats[i].users = ur.value
                }
                if (mr.isSuccess) {
                    chats[i].messages = mr.value
                }
            }
            return {isSuccess: true, value: chats}

        })
    }

    public static async GetUsersForChat(chatId: number): Promise<VResult<User[], RequestException>> {
        return await httpFuncWrapper(async () => {
            let users = (await api.get<UserResponse[]>(apiRoutes.getUsersForChat + `/${chatId}`))
                .data.map(ur => new User(ur.username, ur.email, ur.is_verified))

            return {isSuccess: true, value: users}

        })
    }

    public static async GetMessagesForChat(chatId: number): Promise<VResult<Message[], RequestException>> {
        return await httpFuncWrapper(async () => {
            let messages = (await api.get<MessageResponse[]>(apiRoutes.messages + `/${chatId}`))
                .data.map(m => new Message(m.id, m.text, m.chat.id, m.sending_time))

            return {isSuccess: true, value: messages}

        })
    }

    public static async CreateChat(data: ChatCreateRequest): Promise<VResult<Chat, RequestException>> {
        return await httpFuncWrapper(async () => {
            let chat = (await api.post<ChatResponse, AxiosResponse, ChatCreateRequest>(apiRoutes.createChat, {
                name: data.name,
            })).data as ChatResponse

            return {isSuccess: true, value: new Chat(chat.id, chat.name)}
        })
    }

    public static async EditChatInfo(data: ChatEditPayload): Promise<VResult<Chat, RequestException>> {
        return await httpFuncWrapper(async () => {
            let chat = (await api.put<ChatResponse, AxiosResponse, ChatEditRequest>(apiRoutes.editChat, {
                id: data.id,
                name: data.name,
            })).data as ChatResponse;

            return {isSuccess: true, value: new Chat(chat.id, chat.name)}
        })
    }

    public static async DeleteChat(id: number): Promise<Result<RequestException>> {
        return await httpFuncWrapper(async () => {
            await api.delete<null, AxiosResponse, ChatDeleteRequest>(apiRoutes.deleteChat, {
                data: {
                    chat_id: id
                }
            })

            return {isSuccess: true}
        })
    }
}