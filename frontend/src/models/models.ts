export class User {
    public username: string;
    public email: string;
    public isVerified: boolean


    public constructor(username: string, email: string, isVerified: boolean) {
        this.username = username;
        this.email = email;
        this.isVerified = isVerified;
    }
}


export class Chat {
    public id: number
    public name: string
    public users: User[]
    public messages: Message[]

    public constructor(id: number, name: string, users: User[] = [], messages: Message[] = []) {
        this.id = id;
        this.name = name;
        this.users = users;
        this.messages = messages
    }
}

export class Message{
    public id: number
    public text: string
    public chatId: number
    public sendingTime: Date

    public constructor(id: number, text: string, chatId: number, sendingTime: string) {
        this.id = id
        this.text = text
        this.chatId = chatId
        this.sendingTime = new Date(sendingTime)
    }
}


export class MessageCreate{
    public text: string
    public chat_id: number

    public constructor(text: string, chatId: number) {
        this.text = text
        this.chat_id = chatId
    }
}