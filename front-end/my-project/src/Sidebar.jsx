import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHome, faPlus, faCalendarAlt, faCog, faUser } from '@fortawesome/free-solid-svg-icons';
import logo from './learniverse.png';
import { Link } from 'react-router-dom';

const Sidebar = () => {
  return (
    <div className="bg-blue-950 h-screen w-80 py-4 flex flex-col justify-between">
      <div>
        {/* Logo */}
        <div className="flex items-center px-4 py-2 text-white mb-8">
          <img src={logo} alt="Learniverse Logo" className="h-12 mr-8" />
          <span className="text-lg">Learniverse</span>
        </div>
        {/* Sidebar links */}
        <h2 className=' text-white text-lg'>Menu</h2>
        <Link to="/dashboard" className="flex items-center px-4 py-2 hover:bg-blue-900 text-white mt-4 text-lg">
          <FontAwesomeIcon icon={faHome} className="h-6 w-6 mr-4" />
          <span className="ml-4">Dashboard</span>
        </Link>
        <Link to="/chats" className="flex items-center px-4 py-2  hover:bg-blue-900 text-white text-lg">
          <FontAwesomeIcon icon={faPlus} className="h-6 w-6 mr-4" />
          <span className="ml-4">Chat</span>
        </Link>
        <Link to="/calendar" className="flex items-center px-4 py-2 hover:bg-blue-900 text-white text-lg">
          <FontAwesomeIcon icon={faCalendarAlt} className="h-6 w-6 mr-4" />
          <span className="ml-4">Calendar</span>
        </Link>
        {/* Profile link */}
        <Link to="/profile" className="flex items-center px-4 py-2 hover:bg-blue-900 text-white text-lg">
          <FontAwesomeIcon icon={faUser} className="h-6 w-6 mr-4" />
          <span className="ml-4">Profile</span>
        </Link>
        {/* Settings link */}
        {/* <a href="/profile" className="flex items-center px-4 py-2  hover:bg-blue-900 text-white text-lg">
          <FontAwesomeIcon icon={faCog} className="h-6 w-6 mr-4" />
          <span className="ml-4">Settings</span>
        </a> */}
      </div>
    </div>
  );
};

export default Sidebar;




