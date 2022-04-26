import React from 'react';
import '../styles/footer.css'

function Footer() {
    return (
        <div className="footer">
            <div className="container">
                <div className="footer-body">
                    <div className="copyright">Copyright 2022</div>
                    <div className="links">
                        <div className="about">About</div>
                        <div className="policy">Privacy Policy</div>
                        <div className="policy">Cookies Policy</div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Footer;