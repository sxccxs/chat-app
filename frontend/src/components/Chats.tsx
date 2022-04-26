import React from 'react';
import {Navigate} from "react-router-dom";

import {useSelector} from "react-redux";
import {State} from "../store";
import {routes} from "../resources";
import Header from "./Header";

function Chats() {
    const user = useSelector((state: State) => state.user)
    const chats = useSelector((state: State) => state.chats)


    if (user === null) {
        return <Navigate to={routes.home} replace/>
    }

    return (
        <>
            <Header/>
            <div><h2>chats</h2></div>
            <div>
                {
                    chats.map(c => <div key={c.id}>
                        <h3>{c.name}</h3>
                    </div>)
                }
            </div>
        </>
    );
}

export default Chats;