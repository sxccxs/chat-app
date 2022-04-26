import React, {useEffect, useState} from 'react';
import {useNavigate, useParams} from "react-router-dom";
import {UserService} from "../services";
import "../styles/activation.css"
import {Form} from "./Forms";
import RoundButton from "./RoundButton";
import {routes} from "../resources";

interface RouteParams extends Record<string, string> {
    uid: string,
    token: string
}

function Activation() {
    const navigate = useNavigate();
    const {uid, token} = useParams<RouteParams>() as { uid: string, token: string };
    const [loading, setLoading] = useState<boolean>(true);
    const [success, setSuccess] = useState<boolean>(false);

    useEffect(() => {
        async function activate() {
            let result = await UserService.VerifyEmail(uid, token)
            setSuccess(result.isSuccess)
        }

        activate().then(() => setLoading(false))
    }, [])

    if (loading) {
        return <></>
    }

    if (!success){
        return <div className="activation">
            <Form className="activation-form">
                <div className="form-header">Уупс!</div>
                <p className="activation-text">Щось пішло не так</p>
            </Form>
        </div>;
    }

    return <div className="activation">
        <Form className="activation-form">
            <div className="form-header">Дякуємо</div>
            <p className="activation-text">Ви успішно підтвердили пошту</p>
            <RoundButton text="Увійти" className="activation-button" onClick={() => navigate(routes.login)}/>
        </Form>
    </div>;
}

export default Activation;