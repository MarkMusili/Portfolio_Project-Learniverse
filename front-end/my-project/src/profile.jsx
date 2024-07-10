import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faEnvelope, faPhone, faMapMarkerAlt } from '@fortawesome/free-solid-svg-icons';

const Profile = () => {
  return (
    <div className="max-w-md mx-auto bg-white shadow-lg rounded-lg overflow-hidden">
      <div className="px-6 py-4">
        <div className="flex justify-center">
          <img className="h-24 w-24 rounded-full object-cover" src="https://randomuser.me/api/portraits/men/1.jpg" alt="Profile" />
        </div>
        <div className="text-center mt-4">
          <h1 className="text-xl font-bold text-gray-800">John Doe</h1>
          <p className="text-sm text-gray-600">Frontend Developer</p>
        </div>
      </div>
      <div className="px-6 py-4">
        <div className="flex items-center mb-2">
          <FontAwesomeIcon icon={faEnvelope} className="text-gray-400 h-5 w-5 mr-2" />
          <p className="text-gray-700">john.doe@example.com</p>
        </div>
        <div className="flex items-center mb-2">
          <FontAwesomeIcon icon={faPhone} className="text-gray-400 h-5 w-5 mr-2" />
          <p className="text-gray-700">(123) 456-7890</p>
        </div>
        <div className="flex items-center mb-2">
          <FontAwesomeIcon icon={faMapMarkerAlt} className="text-gray-400 h-5 w-5 mr-2" />
          <p className="text-gray-700">123 Street, City, Country</p>
        </div>
      </div>
      <div className="px-6 pt-4 pb-2">
        <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full focus:outline-none">
          Edit Profile
        </button>
      </div>
    </div>
  );
};

export default Profile;
