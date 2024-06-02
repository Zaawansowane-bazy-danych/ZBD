import { useState, useEffect } from 'react';
import { Input, Button, message } from 'antd';
import 'tailwindcss/tailwind.css';
import { useNavigate } from 'react-router-dom';
import { useUser } from "../../UserContext";

function WelcomeScreen() {
    const [userNameLocal, setUserNameLocal] = useState('');
    const [userName, setUserName] = useUser();

    const navigate = useNavigate(); 

    useEffect(() => {
        if (userName) {
            navigate(`/home/${userName}`);
        }
    }, [userName, navigate]);

    const handleConfirm = () => {
        if (userNameLocal.trim() === '') {
            message.warning('Please enter your name');
        } else {
            setUserName(userNameLocal);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center h-screen">
            <h1 className="text-4xl font-bold mb-8 text-center">Welcome to the Tournament App!</h1>
            <div className="flex flex-col items-center mb-4">
                <Input
                    placeholder="Enter your name"
                    className="w-full md:w-auto text-lg"
                    value={userNameLocal}
                    onChange={(e) => setUserNameLocal(e.target.value)}
                />
            </div>
            <Button type="primary" className="text-lg h-10" onClick={handleConfirm}>
                Confirm
            </Button>
        </div>
    );
}

export default WelcomeScreen;