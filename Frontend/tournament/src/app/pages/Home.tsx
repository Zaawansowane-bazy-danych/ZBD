import React, { useEffect, useState } from 'react';
import { API_URL } from '../../config';
import { Input } from 'antd';

const { TextArea } = Input;

function Home() {
    const [userNames, setUserNames] = useState('');

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
    setUserNames(event.target.value);
    console.log(userNames);
  };

    return (
        <>
            <TextArea
                placeholder="Enter user names"
                autoSize={{ minRows: 3 }}
                value={userNames}
                onChange={handleInputChange}
                style={{
                    width: '25%',
                    margin: '20px auto',
                    display: 'block'
                }}
            />
        </>
    );
}

export default Home;
