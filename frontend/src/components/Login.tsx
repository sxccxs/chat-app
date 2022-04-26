import React, {useEffect, useState} from 'react';
import {bindActionCreators} from "redux";
import {Navigate} from "react-router-dom";
import {Form, FormError, FormField} from "./Forms";
import {
    FormValidationService,
    MAX_EMAIL_LENGTH,
    MAX_PASSWORD_LENGTH, UserService,
} from "../services";
import RoundButton from "./RoundButton";
import {FormStateObject} from "../models";
import {State, userActionCreators} from "../store";
import '../styles/login.css';
import {useDispatch, useSelector} from "react-redux";
import {routes} from "../resources";
import {StatusCodes} from "http-status-codes";

function Login() {
    let email = new FormStateObject<string>(useState(""),
        useState<string | null>(""));
    let password = new FormStateObject<string>(useState(""),
        useState<string | null>(""));

    const fieldsValid = [email, password].map(o => o.error === null);
    let [formValid, setFormValid] = useState<boolean>(false)
    let [credentialsError, setCredentialsError] = useState<boolean>(false);


    useEffect(() => {
        setFormValid(fieldsValid.every(x => x))
    }, [fieldsValid])

    const dispatch = useDispatch()
    const { login } = bindActionCreators(userActionCreators, dispatch)
    const user = useSelector((state: State) => state.user);
    const loginOnClick = async (): Promise<void> => {
        let result = await UserService.Login(email.value, password.value)
        if (result.isSuccess) {
            login(result.value);
            return
        }
        if (result.exception.statusCode === StatusCodes.NOT_FOUND){
            setCredentialsError(true)
        }

        throw result.exception;
    }

    if (user !== null){
        return <Navigate to={routes.root}/>
    }

    return (
        <div className="login">
            {credentialsError && <FormError onClick={() => setCredentialsError(false)} text="Користувача із такими даними не існує"/>}
            <Form className="login-form">
                <div className="form-header">Вхід</div>
                <FormField id="email"
                           obj={email}
                           className="login-input"
                           label="Email"
                           inputType="email"
                           maxLength={MAX_EMAIL_LENGTH}
                           validators={new Map([
                               [FormValidationService.ValidateEmail, email],
                           ])}/>
                <FormField id="password"
                           obj={password}
                           className="login-input"
                           label="Пароль"
                           inputType="password"
                           maxLength={MAX_PASSWORD_LENGTH}
                           validators={new Map([
                               [FormValidationService.ValidateLoginPassword, password],
                           ])}/>
                <RoundButton text="Увійти" disabled={!formValid} className="login-submit"
                             onClick={loginOnClick}/>
            </Form>
        </div>
    );
}

export default Login;