import React from 'react';
import {Navigate} from "react-router-dom";

import {useSelector} from "react-redux";
import {State} from "../store";
import {routes} from "../resources";
import Header from "./Header";

function Chat() {
    const user = useSelector((state: State) => state.user)
    if (user === null) {
        return <Navigate to={routes.home} replace/>
    }

    return (
        <>
            <Header/>
            <div><h2>chat</h2></div>
        </>
    );
}

export default Chat;