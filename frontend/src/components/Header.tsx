import React, {ReactNode} from 'react';
import "../styles/header.css";
import RoundButton from "./RoundButton";
import {Link, NavLink, useNavigate} from "react-router-dom";
import {routes} from "../resources";
import {useDispatch, useSelector} from "react-redux";
import {State, userActionCreators} from "../store";
import {bindActionCreators} from "redux";
import {UserService} from "../services";

function Header() {
    const dispatch = useDispatch()
    const { logout } = bindActionCreators(userActionCreators, dispatch)
    let user = useSelector((state: State) => state.user)

    const loginOnClick = (): void => {
        UserService.Logout()
        logout();
    }

    let navigate = useNavigate();
    return (
        <header>
            <div className="container">
                <div className="navbar">
                    <div className="logo">
                        <Link to={routes.root}><img src="#" alt=""/></Link>
                    </div>
                    <div className="menu">
                        <CNavLink to={routes.home}>Головна</CNavLink>
                        <CNavLink to={routes.download}>Завантажити</CNavLink>
                        <CNavLink to={routes.about}>Про нас</CNavLink>
                    </div>
                    <div className="auth">
                        {user === null ?
                            <>
                                <RoundButton text="Увійти" className={"login-button"}
                                             onClick={() => navigate(routes.login)}/>
                                <RoundButton text="Зареєструватися" className={"registration-button"}
                                             onClick={() => navigate(routes.registration)}/>
                            </>
                            : <>
                                <RoundButton text="Вийти"
                                             className={"registration-button"}
                                             onClick={loginOnClick}/>
                            </>}
                    </div>
                </div>
            </div>
        </header>
    );
}

export default Header;

function CNavLink(props: { children: ReactNode, to: string }) {
    return (
        <NavLink className={({isActive}) => "menu-link" + (isActive ? " active-menu-link" : "")} to={props.to}>
            {props.children}
        </NavLink>
    )
}