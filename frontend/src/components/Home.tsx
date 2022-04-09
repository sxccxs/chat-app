import React from 'react';
import RoundButton from "./RoundButton";
import '../styles/home.css';
import logo from '../images/home-img-1.svg';
import Header from "./Header";


function Home() {
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
                                <RoundButton text="Завантажити" className={"download"}/>
                            </div>
                            <div className="img"><img src={logo} alt="chat app"/></div>
                        </div>
                    </div>
                </section>
                {/*<section className="section2">*/}
                {/*    <div className="container">*/}
                {/*        <div className="content">*/}
                {/*            <div className="text">*/}
                {/*                <div className="header">ЩОСЬ ТИПУ СЛОГАНА ЧИ ГОЛОВНИХ ТЕЗИСІВ</div>*/}
                {/*                <div className="article">просто якийсь текст поки що хай буде тут бла, бла, бла, має*/}
                {/*                    бути*/}
                {/*                    більше тексту*/}
                {/*                </div>*/}
                {/*            </div>*/}
                {/*            <div className="icons"></div>*/}
                {/*        </div>*/}
                {/*    </div>*/}
                {/*</section>*/}
            </main>
        </>
    );
}

export default Home;