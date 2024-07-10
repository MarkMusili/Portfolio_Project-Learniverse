import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { GoogleLogin } from 'react-oauth-google';

const Signup = () => {
  const [fullName, setFullName] = useState('');
  const [age, setAge] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  // Function to handle login success
  const handleLoginSuccess = (response) => {
    console.log('Login Successful:', response);
    // Implement your login logic here
    // For example, set the user data in state or localStorage
  };

  // Function to handle login failure
  const handleLoginFailure = (response) => {
    console.error('Login Failed:', response);
    // Handle login failure (show error message, etc.)
  };

  // Function to handle form submission
  const handleSubmit = (event) => {
    event.preventDefault();
    // Implement form submission logic
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <div className="relative flex w-full max-w-3xl overflow-hidden bg-white rounded-lg shadow-lg">
        <div className="w-1/2">
          <img
            className="object-cover w-full h-full"
            src="https://media.istockphoto.com/id/1320882544/photo/glowing-light-bulb-and-book-or-text-book-with-futuristic-icon-self-learning-or-education.jpg?b=1&s=612x612&w=0&k=20&c=swIaRrs2C2hxbbzcvRlY29LIz6VPi3L2X2eVhWcn7go="
            alt="Learniverse"
          />
        </div>
        <div className="relative z-10 w-1/2 p-8">
          <h2 className="text-2xl font-semibold text-center text-gray-700">Sign Up</h2>
          <p className="text-xl text-center text-gray-600">Create a new account</p>

          {/* Google Sign-In Button */}
          <GoogleLogin
            clientId="YOUR_GOOGLE_CLIENT_ID"
            buttonText="Sign up with Google"
            onSuccess={handleLoginSuccess}
            onFailure={handleLoginFailure}
            cookiePolicy={'single_host_origin'}
            className="w-full mt-4 text-gray-600 transition-colors duration-200 transform border rounded-lg hover:bg-gray-50 p-2"
          />

          <div className="flex items-center justify-between mt-4">
            <span className="w-1/5 border-b lg:w-1/4"></span>
            <span className="text-xs text-gray-500 uppercase">or sign up with email</span>
            <span className="w-1/5 border-b lg:w-1/4"></span>
          </div>

          <form onSubmit={handleSubmit} className="mt-4">
            <div className="mt-4">
              <label htmlFor="fullName" className="block mb-2 text-sm font-medium text-gray-600">Full Name</label>
              <input
                id="fullName"
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                className="block w-full px-4 py-2 mt-2 text-gray-700 bg-white border rounded-md focus:border-blue-500 focus:ring-blue-500 focus:outline-none focus:ring focus:ring-opacity-40"
                placeholder="Enter full name"
              />
            </div>

            <div className="mt-4">
              <label htmlFor="age" className="block mb-2 text-sm font-medium text-gray-600">Age</label>
              <input
                id="age"
                type="number"
                value={age}
                onChange={(e) => setAge(e.target.value)}
                className="block w-full px-4 py-2 mt-2 text-gray-700 bg-white border rounded-md focus:border-blue-500 focus:ring-blue-500 focus:outline-none focus:ring focus:ring-opacity-40"
                placeholder="Enter age"
              />
            </div>

            <div className="mt-4">
              <label htmlFor="email" className="block mb-2 text-sm font-medium text-gray-600">Email Address</label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="block w-full px-4 py-2 mt-2 text-gray-700 bg-white border rounded-md focus:border-blue-500 focus:ring-blue-500 focus:outline-none focus:ring focus:ring-opacity-40"
                placeholder="Enter email address"
              />
            </div>

            <div className="mt-4">
              <label htmlFor="password" className="block mb-2 text-sm font-medium text-gray-600">Password</label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="block w-full px-4 py-2 mt-2 text-gray-700 bg-white border rounded-md focus:border-blue-500 focus:ring-blue-500 focus:outline-none focus:ring focus:ring-opacity-40"
                placeholder="Enter password"
              />
            </div>

            <div className="mt-8">
              <button type="submit" className="w-full px-4 py-2 tracking-wide text-white transition-colors duration-200 transform bg-blue-700 rounded-md hover:bg-gray-600 focus:outline-none focus:bg-gray-600">
                Sign Up
              </button>
            </div>
          </form>

          <div className="flex items-center justify-between mt-4">
            <span className="w-1/5 border-b lg:w-1/4"></span>
            <Link to="/login" className="text-xs text-blue-500 uppercase hover:underline">or sign up</Link>
            <span className="w-1/5 border-b lg:w-1/4"></span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Signup;
