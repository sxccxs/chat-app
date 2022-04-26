import React from 'react';
import RoundButton from "./RoundButton";
import '../styles/home.css';
import img1 from '../images/home-img-1.svg';
import img2 from '../images/home-img-2.svg';
import Header from "./Header";
import {routes} from "../resources";
import {useNavigate} from "react-router-dom";
import Footer from "./Footer";


function Home() {

    const navigate = useNavigate();
    return (
        <>
            <Header/>
            <main>
                <section className="section1">
                    <div className="container">
                        <div className="content">
                            <div className="text">
                                <div className="header">ЛОРЕМ ІПСУМ</div>
                                <div className="article">просто якийсь текст поки що хай буде тут бла, бла, бла, має
                                    бути
                                    більше
                                    тексту, ну, приблизно так
                                </div>
                                <RoundButton text="Завантажити" onClick={() => navigate(routes.download)} className={"download"}/>
                            </div>
                            <div className="img"><img src={img1} alt="chat app"/></div>
                        </div>
                    </div>
                </section>
                <section className="section2">
                    <div className="container">
                        <div className="content">
                            <div className="text">
                                <div className="header">ЩОСЬ ТИПУ СЛОГАНА ЧИ ГОЛОВНИХ ТЕЗИСІВ</div>
                                <div className="article">просто якийсь текст поки що хай буде тут бла, бла, бла, має
                                    бути
                                    більше тексту
                                </div>
                            </div>
                            <div className="icons">
                                <div className="icon"></div>
                                <div className="icon"></div>
                                <div className="icon"></div>
                                <div className="icon"></div>
                                <div className="icon"></div>
                            </div>
                        </div>
                    </div>
                </section>
                <section className="section3">
                    <div className="container">
                        <div className="content">
                            <div className="img"><img src={img2} alt="chat app"/></div>
                            <div className="text">
                                <div className="header">ЛОРЕМ ІПСУМ</div>
                                <div className="article">просто якийсь текст поки що хай буде тут бла, бла, бла, має
                                    бути
                                    більше
                                    тексту, ну, приблизно так
                                </div>
                            </div>

                        </div>
                    </div>
                </section>
            </main>
            <Footer/>
        </>
    );
}

export default Home;