import React, { useEffect, useState } from 'react';
import { API_URL } from '../../config';
import { Input, Button, message } from 'antd';
import { useUser } from "../../UserContext";
import { useNavigate } from 'react-router-dom';
import { SaveOutlined } from '@ant-design/icons';

const { TextArea } = Input;

function Home() {
    const [userNames, setUserNames] = useState<string[]>([]);
    const [tournament, setTournament] = useState<TournamentModel | null>(null);  
    const [isValid, setIsValid] = useState(true);
    const [userName ] = useUser();
    const navigate = useNavigate();
    const [isSubmitted, setIsSubmitted] = useState(false); 
    const [scores, setScores] = useState<{ [key: string]: number }>({});
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        setUserNames(['1', '2', '3', '4', '5', '6', '7', '8']);
        if (!userName) {
            navigate(`/`);
        }
    }, [userName, navigate]);

    const fetchWithTimeout = (url: string, options: RequestInit, timeout: number = 2000) => {
        return new Promise<Response>((resolve, reject) => {
            const timer = setTimeout(() => {
                message.error('Request timed out');
                reject(new Error('Request timed out'));
            }, timeout);

            fetch(url, options)
                .then(response => {
                    clearTimeout(timer);
                    resolve(response);
                })
                .catch(err => {
                    clearTimeout(timer);
                    message.error('Request failed: ' + err.message);
                    reject(err);
                });
        });
    };

    const createTournament = (data: string[]) => {
        fetchWithTimeout(API_URL + 'tournament/' || '', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ player_names: data }),
        })
        .then(response => response.json())
        .then(json => {
            setTournament(json);
        })
        .catch(error => {
            console.error('Error creating tournament:', error);
        });
    };

    const updateTournament = (data: any) => {
        setLoading(true);
        const updateData = data.update_data;  
        fetchWithTimeout(API_URL + `tournament/${data.tournament_id}` || '', {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(updateData),
        })
        .then(response => response.json())
        .then(json => {
            if(json?.matches) {
                setTournament(json);
            }
            setLoading(false);
        })
        .catch(error => {
            console.error('Error updating tournament:', error);
            setLoading(false);
        });
    };

    const handleInputChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
        const value = event.target.value;
        setUserNames(value.split('\n'));
        validateUserNames(value);
    };

    const validateUserNames = (value: string) => {
        const names = value.split('\n');
        const isValidFormat = names.every(name => name.trim().split(' ').length === 1);
        setIsValid(isValidFormat);
    };

    const handleSubmit = async () => {
        if (isValid) {
            message.success('User names submitted successfully!');
            createTournament(userNames);
            setIsSubmitted(true); 
        } else {
            message.error('Please enter one-word user names separated by new lines.');
        }
    };

    const handleScoreChange = (match: MatchModel, player: string) => (event: React.ChangeEvent<HTMLInputElement>) => {
        const value = parseFloat(event.target.value);
        setScores(prevScores => ({
            ...prevScores,
            [`${match.level}-${match.number}-${player}`]: value
        }));
    };

    const saveScore = (match: MatchModel, player: string) => async () => {
        let playerName = '';
        let score = 0;
        if (player === 'left') {
            match.score_left = scores[`${match.level}-${match.number}-left`] || 0;
            playerName = match.player_left?.name || '';
            score = match.score_left;
        } else if (player === 'right') {
            match.score_right = scores[`${match.level}-${match.number}-right`] || 0;
            playerName = match.player_right?.name || '';
            score = match.score_right;
        }
        
        tournament?.matches.forEach((levelMatches) => {
            levelMatches.forEach((iteratedMatch) => {
                if(iteratedMatch.level === match.level && iteratedMatch.number === match.number) {
                    iteratedMatch = match;
                }
            })
        });
        updateTournament({ tournament_id: tournament?.id, update_data: {level: match.level, level_number: match.number, player_name: playerName, score: score} });
    }

    return (
        <div style={{ display: 'flex', alignItems: 'center', flexDirection: 'column' }}>
            <TextArea
                placeholder="Enter user names (split with new lines)"
                autoSize={{ minRows: 3 }}
                value={userNames.join('\n')}
                onChange={handleInputChange}
                style={{
                    width: '15%',
                    height: '25%',
                    margin: '20px auto',
                }}
                disabled={isSubmitted} 
            />
            <Button
                type="primary"
                onClick={handleSubmit}
                style={{ width: '15%', margin: '0 auto' }}
                size="large"
                disabled={isSubmitted} 
            >
                Submit
            </Button>

            {tournament &&
                <div className='flex flex-row m-6'>
                    {
                        tournament.matches.map((levelMatches, index) => (
                            <div key={index} className="flex flex-col justify-center first-letter:items-center"> 
                                {
                                    levelMatches.map((match, index) => (
                                        <div key={index} className='flex flex-col mb-4 ml-12'>
                                            <div className='flex'>
                                                <div className='bg-gray-200 rounded-none pr-1 pl-1 w-36 text-center' style={{ border: '1px solid #d9d9d9' }}>{match.player_right?.name}</div>
                                                <Input 
                                                    className="w-24 rounded-none"
                                                    style={{ textAlign: 'center', border: '1px solid #d9d9d9' }}
                                                    disabled={!match.player_right?.name}
                                                    defaultValue={match.score_right}
                                                    onChange={handleScoreChange(match, 'right')}
                                                    type="number"
                                                    
                                                />
                                                <Button style={{ border: '1px solid #d9d9d9' }} className='cursor-pointer text-xl pl-1 pr-1 border rounded-none border-l-0 border-b-0' onClick={saveScore(match, 'right')} icon={<SaveOutlined className='text-xl'/>} disabled={loading}></Button>
                                            </div>
                                            <div className='flex'>
                                                <div className='bg-gray-200 rounded-none pr-1 pl-1 w-36 text-center' style={{ border: '1px solid #d9d9d9' }}>{match.player_left?.name}</div>
                                                <Input 
                                                    className="w-24 rounded-none"
                                                    style={{ textAlign: 'center', border: '1px solid #d9d9d9' }}
                                                    disabled={!match.player_left?.name}
                                                    defaultValue={match.score_left}
                                                    onChange={handleScoreChange(match, 'left')}
                                                    type="number"
                                                />
                                                {/* <SaveOutlined /> */}
                                                <Button style={{ border: '1px solid #d9d9d9' }} className='cursor-pointer pl-1 pr-1 rounded-none border-l-0' onClick={saveScore(match, 'left')} icon={<SaveOutlined className='text-xl' />} disabled={loading}></Button>
                                            </div>
                                        </div>
                                    ))
                                }
                            </div>
                        ))
                    }
                </div>
            }
        </div>
    );
}

export default Home;

export interface TournamentModel {
    id: string;
    matches: MatchModel[][];
}

export interface MatchModel {
    level: number;
    number: number;
    player_left: Player;
    player_right: Player;
    score_left: number;
    score_right: number;
    winner: Player;
}

export interface Player {
    name: string;
}
