import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import TradingBot from './components/TradingBot'
import LandingPage from "./components/LandingPage";
import Registration from "./components/Registration";
import LogIn from "./components/LogIn";

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<LandingPage />} />
        <Route exact path="/register" element={<Registration />} />
        <Route exact path="/sign-in" element={<LogIn />} />
        <Route exact path="/trading-bot" element={<TradingBot />} />
      </Routes>
    </Router>
  );
}

export default App;
