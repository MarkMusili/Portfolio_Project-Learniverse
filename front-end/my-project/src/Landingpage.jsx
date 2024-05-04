import React from 'react';
import { BrowserRouter as Router, Link } from 'react-router-dom';
import logo from './learniverse.png';

const LandingPage = () => {
  return (
    <div className="bg-blue-500 min-h-screen flex flex-col justify-center items-center overflow-hidden">
      <img src={logo} alt="Learniverse" className="w-48 h-48 mb-8 animate-fade-in-down" /> {/* Adjusted size */}

      <h1 className="text-4xl md:text-6xl text-white font-bold mb-4 text-center animate-fade-in-up">Unlock Your Potential</h1>
      <p className="text-lg md:text-xl text-white mb-8 text-center max-w-md animate-fade-in">Discover new skills and reach new heights with our interactive learning platform.</p>

      <button to="/login" className="bg-white text-blue-500 hover:bg-blue-600 hover:text-white py-3 px-8 rounded-full text-lg md:text-xl font-semibold transition duration-300 ease-in-out animate-bounce">Get Started</button>
    </div>
  );
};

export default LandingPage;
