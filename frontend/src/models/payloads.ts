import React from "react";

export class FormStateObject<T> {
    value: T;
    setValue: React.Dispatch<React.SetStateAction<T>>;
    error: string | null;
    setError: React.Dispatch<React.SetStateAction<string | null>>;


    constructor(v1: [T, React.Dispatch<React.SetStateAction<T>>],
                v2: [string | null, React.Dispatch<React.SetStateAction<string | null>>]) {
        [this.value, this.setValue] = v1;
        [this.error, this.setError] = v2;
    }

}


export class RequestException {
    statusCode: number
    message: string

    constructor(statusCode: number, message: string) {
        this.statusCode = statusCode
        this.message = message
    }
}

export class RegistrationData {
    username: string
    email: string
    password: string
    rePassword: string

    constructor(username: string, email: string, password: string, rePassword: string) {
        this.username = username
        this.email = email
        this.password = password
        this.rePassword = rePassword
    }
}