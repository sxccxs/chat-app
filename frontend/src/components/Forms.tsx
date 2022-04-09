import React, {ReactNode, useState} from 'react';
import '../styles/form.css';
import {FormStateObject} from "../models";

function Form(props: { className?: string, children: ReactNode[] | ReactNode }) {
    return (
        <div className={`form ${props.className}`}>
            {props.children}
        </div>
    );
}

type FieldValidator = (field: string) => string | null


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
    const onInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        e.preventDefault()
        let value = e.target.value;
        if (props.validators){
            for (let [valid, obj] of props.validators.entries()) {
                obj.setError(valid(value))
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
                {props.maxLength &&
                    <span className="max-length-counter">{props.obj.value.length}/{props.maxLength}</span>
                }
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
            <span onClick={props.onClick} className="form-error__cross">&times;</span>
        </div>
    )
}

export {Form, FormField, FormError};

