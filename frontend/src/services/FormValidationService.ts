export const MIN_USERNAME_LENGTH = 3;
export const MAX_USERNAME_LENGTH = 30;
export const MAX_EMAIL_LENGTH = 50;
export const MIN_PASSWORD_LENGTH = 8;
export const MAX_PASSWORD_LENGTH = 50;

export class FormValidationService {

    public static ValidateUsername(username: string): string | null {
        if (username === null || username.length < MIN_USERNAME_LENGTH) {
            return `Мінімум ${MIN_USERNAME_LENGTH} символів`
        }
        if (username.match(/[^0-9a-z_]+/i)) {
            return "Може мати лише літери, цифри та '_'"
        }
        if (!username[0].match(/[a-z]/i)) {
            return "Має починатися з літери"
        }
        return null;
    }

    public static ValidateEmail(email: string): string | null {
        const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        if (!email.match(re)) {
            return "Некоректний email"
        }
        return null
    }

    public static ValidatePassword(password: string): string | null {
        if (password === null || password.length < MIN_PASSWORD_LENGTH) {
            return "Мінімум 8 символів"
        }
        if (!password.match(/[a-z]/)){
            return "Має містити хоча б одну малу літеру"
        }
        if (!password.match(/[A-Z]/)){
            return "Має містити хоча б одну велику літеру"
        }
        if (!password.match(/[0-9]/)){
            return "Має містити хоча б одну цифру"
        }
        if (!password.match(/[!-\/:-@[-`{-~]/)){
            return "Має містити хоча б один символ"
        }

        return null;
    }

    public static ValidateRePassword(password:string, rePassword: string): string | null{
        if (password !== rePassword){
            return "Паролі повинні збігатися"
        }

        return null;
    }

    public static ValidateLoginPassword(password: string): string | null{
        if (password === null || password.length === 0){
            return "Пароль не може бути порожнім"
        }

        return null;
    }
}