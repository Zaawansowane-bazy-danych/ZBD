import React, { useEffect, useState } from 'react';
import { useUser } from "../../UserContext";
import { useNavigate } from 'react-router-dom';
import { useTournament } from '../../UserContext';
import { API_URL } from '../../config';
import { Button, Input, Modal } from 'antd';


function Tournament() {
    const [userName, setUserName] = useUser();
    const navigate = useNavigate(); 
    const [tournamentsList, setTournamentsList] = useTournament();
    const [tournamentsData, setTournamentsData] = useState<TournamentModel[]>([]);

    useEffect(() => {
        console.log(tournamentsList);
        if(!userName) {
            navigate(`/`);
        }
    }, [userName, navigate]);

    useEffect(() => {
        const fetchTournaments = async () => {
            const data = await Promise.all(tournamentsList.map(async (id) => {
                const response = await fetch(`${API_URL}tournament/${id}`);
                const tournament = await response.json();
                return tournament;
            }));
            setTournamentsData(data);
            console.log(data);
        };
        fetchTournaments();
    }, [tournamentsList]);

    return (
        <div>
            {tournamentsData &&
                <div>
                    {
                        tournamentsData.map((tournament, index) => (
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
                                                                disabled={true}
                                                                defaultValue={match.score_right}
                                                                type="number"    
                                                            />
                                                        </div>
                                                        <div className='flex'>
                                                            <div className='bg-gray-200 rounded-none pr-1 pl-1 w-36 text-center' style={{ border: '1px solid #d9d9d9' }}>{match.player_left?.name}</div>
                                                            <Input 
                                                                className="w-24 rounded-none"
                                                                style={{ textAlign: 'center', border: '1px solid #d9d9d9' }}
                                                                disabled={true}
                                                                defaultValue={match.score_left}
                                                                type="number"
                                                            />
                                                        </div>
                                                    </div>
                                                ))
                                            }
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

export default Tournament;

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