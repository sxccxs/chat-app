import React, {useEffect, useState} from 'react';
import {useParams} from "react-router-dom";
import {UserService} from "../services";

interface RouteParams extends Record<string, string> {
    uid: string,
    token: string
}

function Activation() {
    const {uid, token} = useParams<RouteParams>() as { uid: string, token: string };
    const [loading, setLoading] = useState<boolean>(true);
    const [success, setSuccess] = useState<boolean>(false);

    useEffect(() => {
        async function activate() {
            let result = await UserService.Activate(uid, token)
            setSuccess(result.isSuccess)
        }

        activate().then(() => setLoading(false))
    }, [])

    if (loading) {
        return <></>
    }

    return (<>
            <div>Activation</div>
            <div>{success ? "Ok" : "Error"}</div>
        </>
    );
}

export default Activation;