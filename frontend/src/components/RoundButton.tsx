import React from 'react';
import '../styles/round-button.css';

interface RoundButtonProps {
    text: string,
    className: string,
    disabled?: boolean,
    onClick?: React.MouseEventHandler
}

const RoundButton: React.FC<RoundButtonProps> = (props) => {
    return (
        <button disabled={props.disabled} className={`round-button ${props.className}`}
                onClick={props.onClick}>
            <p>{props.text}</p>
        </button>

    );
}
RoundButton.defaultProps = {
    disabled: false,
}

export default RoundButton;