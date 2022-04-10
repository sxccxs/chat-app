import React, {useCallback, useEffect, useState} from 'react';
import {FieldValidator, Form, FormField} from "./Forms";
import '../styles/registration.css';
import RoundButton from "./RoundButton";
import {
    FormValidationService,
    MAX_EMAIL_LENGTH, MAX_PASSWORD_LENGTH,
    MAX_USERNAME_LENGTH, UserService
} from "../services";
import {FormStateObject} from "../models";
import {StatusCodes} from "http-status-codes";


function Registration() {

    let username = new FormStateObject<string>(useState(""),
        useState<string | null>(""))
    let email = new FormStateObject<string>(useState(""),
        useState<string | null>(""));
    let password = new FormStateObject<string>(useState(""),
        useState<string | null>(""));
    let rePassword = new FormStateObject<string>(useState(""),
        useState<string | null>(""));

    const validateRePassword = useCallback(
        (rePassword: string) => {
            return FormValidationService.ValidateRePassword(password.value, rePassword)
        },
        [password.value],
    );

    const validatePassword = useCallback(
        (password: string) => {
            return FormValidationService.ValidateRePassword(password, rePassword.value)
        },
        [rePassword.value],
    );


    const validateEmail = async (email: string): Promise<string | null> => {
        let result = await UserService.EmailExists(email)
        if (result.isSuccess){
            return "Email уже зайнятий."
        }

        return null;
    }


    const fieldsValid = [username, email, password, rePassword].map(x => x.error === null);
    let [formValid, setFormValid] = useState<boolean>(false)
    const registrationOnClick = async (): Promise<void> => {
        let result = await UserService.Register({
            username: username.value,
            email: email.value,
            password: password.value,
            rePassword: rePassword.value,
        });

        if (!result.isSuccess) {
            throw result.exception
        }
    }


    useEffect(() => {
        setFormValid(fieldsValid.every(x => x))
    }, [fieldsValid])

    return (
        <div className="registration">
            <Form className="registration-form">
                <div className="registration-header">Реєстрація</div>
                <FormField id="username"
                           obj={username}
                           className="registration-input"
                           label="Ім'я користувача"
                           maxLength={MAX_USERNAME_LENGTH}
                           validators={new Map([
                               [FormValidationService.ValidateUsername, username]
                           ])}/>
                <FormField id="email"
                           obj={email}
                           className="registration-input"
                           label="Email"
                           inputType="email"
                           maxLength={MAX_EMAIL_LENGTH}
                           validators={new Map<FieldValidator, FormStateObject<string>>([
                               [FormValidationService.ValidateEmail, email],
                               [validateEmail, email],
                           ])}/>
                <FormField id="password"
                           obj={password}
                           className="registration-input"
                           label="Пароль"
                           inputType="password"
                           maxLength={MAX_PASSWORD_LENGTH}
                           validators={new Map([
                               [FormValidationService.ValidatePassword, password],
                               [validatePassword, rePassword],
                           ])}/>
                <FormField id="rePassword"
                           obj={rePassword}
                           className="registration-input"
                           label="Підтвердити пароль"
                           inputType="password"
                           maxLength={MAX_PASSWORD_LENGTH}
                           validators={new Map([
                               [validateRePassword, rePassword]
                           ])}/>

                <RoundButton text="Зареєструватися" disabled={!formValid} className="registration-submit"
                             onClick={registrationOnClick}/>
            </Form>
        </div>
    );
}

export default Registration;