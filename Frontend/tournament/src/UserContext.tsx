import React, { createContext, useContext, useState, ReactNode, Dispatch, SetStateAction } from 'react';

type UserContextType = [string, Dispatch<SetStateAction<string>>];
type TournamentContextType = [string[], Dispatch<SetStateAction<string[]>>];

const UserContext = createContext<UserContextType>(['', () => {}]);
const TournamentContext = createContext<TournamentContextType>([[], () => {}]);

interface UserProviderProps {
  children: ReactNode;
}

export const UserProvider = ({ children }: UserProviderProps) => {
  const userState = useState('');
  const tournamentState = useState<string[]>([]);
  
  return (
    <UserContext.Provider value={userState}>
      <TournamentContext.Provider value={tournamentState}>
        {children}
      </TournamentContext.Provider>
    </UserContext.Provider>
  );
};

export const useUser = () => useContext(UserContext);
export const useTournament = () => useContext(TournamentContext);
