import React, {ReactNode} from 'react';
import '../styles/form.css';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faXmark, faCheck} from '@fortawesome/free-solid-svg-icons'
import {FormStateObject} from "../models";

function Form(props: { className?: string, children: ReactNode[] | ReactNode }) {
    return (
        <div className={`form ${props.className}`}>
            {props.children}
        </div>
    );
}

export type FieldValidator = ((field: string) => string | null) | ((field: string) => Promise<string | null>)


interface FormFieldProps {
    id: string,
    label: string,
    obj: FormStateObject<string>,
    inputType?: string,
    className?: string,
    maxLength?: number,
    validators?: Map<FieldValidator, FormStateObject<string>>
}


const FormField: React.FC<FormFieldProps> = (props) => {
    const onInputChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
        e.preventDefault()
        let value = e.target.value;
        if (props.validators) {
            for (let [valid, obj] of props.validators.entries()) {
                let result = valid(value);
                if (result instanceof Promise) {
                    result = await result;
                }
                obj.setError(result)

                if (result !== null) {
                    break;
                }
            }
        }
        props.obj.setValue(value);
    }


    return (
        <div className={`form-field${props.className ? ` ${props.className}` : ""}`}>
            <label htmlFor={props.id} className="inp">
                <input maxLength={props.maxLength} id={props.id}
                       value={props.obj.value} onChange={onInputChange}
                       type={props.inputType} placeholder="&nbsp;"/>
                <span className="label">{props.label}</span>
                <span className="error">{props.obj.error}</span>
                {props.maxLength && props.obj.error !== null &&
                    <span className="max-length-counter">{props.obj.value.length}/{props.maxLength}</span>
                }
                {props.obj.error === null && <span className="correct"><FontAwesomeIcon icon={faCheck}/></span>}
            </label>
        </div>
    );
}

FormField.defaultProps = {
    inputType: "text",
}

function FormError(props: {
    text: string,
    onClick: React.MouseEventHandler
}) {
    return (
        <div className="form-error">
            <p>{props.text}</p>
            <span onClick={props.onClick} className="form-error__cross">
                <FontAwesomeIcon icon={faXmark}/>
            </span>
        </div>
    )
}

export {Form, FormField, FormError};

