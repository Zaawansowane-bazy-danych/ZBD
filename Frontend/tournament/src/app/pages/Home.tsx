import React, { useEffect, useState } from 'react';
import { API_URL } from '../../config';
import { Input, Button, message } from 'antd';
import { useUser } from "../../UserContext";
import { useNavigate } from 'react-router-dom';

const { TextArea } = Input;

function Home() {
    const [userNames, setUserNames] = useState('');
    const [isValid, setIsValid] = useState(true);
    const [userName, setUserName] = useUser();
    const navigate = useNavigate(); 

    useEffect(() => {
        if(!userName) {
            navigate(`/`);
        }
    }, [userName, navigate]);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const response = await fetch(API_URL || '');
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    const handleInputChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
        const value = event.target.value;
        setUserNames(value);
        validateUserNames(value);
    };

    const validateUserNames = (value: string) => {
        const names = value.split('\n');
        const isValidFormat = names.every(name => name.trim().split(' ').length === 1);
        setIsValid(isValidFormat);
    };

    const handleSubmit = () => {
        if (isValid) {
            // Do something with valid user names
            message.success('User names submitted successfully!');
        } else {
            message.error('Please enter one-word user names separated by new lines.');
        }
    };

    return (
        <div style={{display: 'flex', alignItems: 'center', flexDirection: 'column'}}>
            <TextArea
                placeholder="Enter user names (split with new lines)"
                autoSize={{ minRows: 3 }}
                value={userNames}
                onChange={handleInputChange}
                style={{
                    width: '15%',
                    height: '25%',
                    margin: '20px auto',
                }}
            />
            <Button type="primary" onClick={handleSubmit} style={{ width: '15%', margin: '0 auto'}} size="large">Submit</Button>
        </div>
    );
}

export default Home;
