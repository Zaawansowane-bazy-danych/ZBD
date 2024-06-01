import React, { useEffect } from 'react';
import { useUser } from "../../UserContext";
import { useNavigate } from 'react-router-dom';

function Tournament() {
    const [userName, setUserName] = useUser();
    const navigate = useNavigate(); 

    useEffect(() => {
        if(!userName) {
            navigate(`/`);
        }
    }, [userName, navigate]);

    return (
        <></>
    );
}

export default Tournament;
