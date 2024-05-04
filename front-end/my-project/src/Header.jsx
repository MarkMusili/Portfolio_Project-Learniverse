import React, { useState } from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch, faMoon, faBell } from '@fortawesome/free-solid-svg-icons';
import { faHome, faPlus, faCalendarAlt, faCog } from '@fortawesome/free-solid-svg-icons';
import { faList, faThLarge } from '@fortawesome/free-solid-svg-icons';

function Header(){
    const [isDarkMode, setIsDarkMode] = useState(false);

    const toggleDarkMode = () => {
        setIsDarkMode(!isDarkMode);
    };

    return(
        <div className={`bg-${isDarkMode ? 'blue-950' : 'white'} shadow-md rounded-lg`}>
            <div className="max-w-screen-xl mx-auto px-8 sm:px-8 lg:px-8"> {/* Adjust max-w-screen-xl for larger width */}
                <div className="flex justify-between items-center py-6">
                    <div className="flex items-center space-x-4">
                        <span className={`bg-${isDarkMode ? 'blue-500' : 'blue-950'} rounded-full h-10 w-10 flex items-center justify-center text-white animate-pulse`}>
                            <span className="text-xl">D</span>
                        </span>
                        <p className={`text-xl font-semibold ${isDarkMode ? 'text-white' : 'text-gray-800'}`}>Dashboard</p>
                        <div className="ml-0 relative">
                            <input className={`rounded-lg py-3 px-8 w-96 bg-white : 'blue-950'} border border-gray-300 focus:outline-none focus:border-blue-500 text-lg`} type="text" placeholder="Search" />
                            <FontAwesomeIcon icon={faSearch} className={`absolute right-3 top-2 h-6 w-6 text-gray-400 hover:text-gray-700 transition duration-300`} />
                        </div>
                    </div>
                    <div className="flex items-center space-x-4">
                        <button className="text-gray-500 hover:text-gray-700 focus:outline-none" onClick={toggleDarkMode}>
                            <FontAwesomeIcon icon={faMoon} className="h-6 w-6" />
                        </button>
                        <button className="text-gray-500 hover:text-gray-700 focus:outline-none">
                            <FontAwesomeIcon icon={faBell} className="h-6 w-6" />
                        </button>
                        <button className="flex items-center space-x-2 text-gray-700 hover:text-gray-900 focus:outline-none">
                            <div className="h-8 w-8 bg-gray-300 rounded-full"></div>
                            <span  className={isDarkMode ? 'text-white' : 'text-gray-800'}>John Doe</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Header;


