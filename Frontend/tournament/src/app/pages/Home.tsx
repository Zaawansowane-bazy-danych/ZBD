import React, { useEffect, useState } from 'react';
import { API_URL } from '../../config';

function Home() {
    const [data, setData] = useState([]);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const response = await fetch(API_URL || '');
            const jsonData = await response.json();
            setData(jsonData);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    return (
        <div>
        </div>
    );
}

export default Home;
