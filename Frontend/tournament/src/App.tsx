import './App.css';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from './app/pages/Layout';
import WelcomeScreen from './app/pages/WelcomeScreen';
import Home from './app/pages/Home';
import Tournament from './app/pages/Tournament';
import { UserProvider } from './UserContext';

function App() {

  return (
    <UserProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout/>}>
            <Route index element={<WelcomeScreen/>} />
            <Route path="home/:id" element={<Home />} />
            <Route path="tournament" element={<Tournament/>} />
          </Route>
        </Routes>
      </BrowserRouter>
    </UserProvider>
  );
}

export default App;
