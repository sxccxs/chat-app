import React, {useEffect, useState} from 'react';
import {
    BrowserRouter as Router,
    Routes,
    Route,
} from "react-router-dom";
import "./styles/app.css";
import "./normalize.css";
import Home from "./components/Home";
import Tmp from "./components/Tmp";
import Registration, {RegistrationCompleted} from "./components/Registration";
import Login from "./components/Login";
import {routes} from "./resources";
import {UserService} from "./services";
import {useDispatch} from "react-redux";
import {userActionCreators} from "./store";
import {bindActionCreators} from "redux";
import Chats from "./components/Chats";
import Activation from "./components/Activation";

function App() {
    const dispatch = useDispatch()
    const {login} = bindActionCreators(userActionCreators, dispatch)
    const [isLoading, setIsLoading] = useState<boolean>(true)

    useEffect(() => {
        async function auth(): Promise<void> {
            setIsLoading(true)
            let result = await UserService.GetUser()
            if (result.isSuccess) {
                login(result.value)
            }
        }

        auth().then(() => setIsLoading(false))
    }, [])

    if (isLoading) {
        return <></>
    }

    return (
        <div className="App">
            <Router>
                <Routes>
                    <Route path={routes.root} element={<Chats/>}/> :
                    <Route path={routes.home} element={<Home/>}/>
                    <Route path={routes.download} element={<Tmp/>}/>
                    <Route path={routes.about} element={<Tmp/>}/>
                    <Route path={routes.registration} element={<Registration/>}/>
                    <Route path={routes.registrationCompleted} element={<RegistrationCompleted/>}/>
                    <Route path={routes.login} element={<Login/>}/>
                    <Route path={routes.activateFull} element={<Activation/>}/>
                </Routes>
            </Router>
        </div>
    );
}

export default App;
