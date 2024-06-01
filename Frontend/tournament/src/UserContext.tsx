import React, { createContext, useContext, useState, ReactNode } from 'react';

const UserContext = createContext<[string, (user: string) => void]>(['', () => {}]);

interface UserProviderProps {
  children: ReactNode;
}

export const UserProvider = ({ children }: UserProviderProps) => {
  const state = useState('');
  return <UserContext.Provider value={state}>{children}</UserContext.Provider>
};

export const useUser = () => useContext(UserContext);
