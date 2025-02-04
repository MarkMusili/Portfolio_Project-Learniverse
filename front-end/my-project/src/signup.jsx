import React, { useState } from 'react';
import { Link, useHistory } from 'react-router-dom';
import { useAuth } from './AuthContext'; // Ensure correct path
import { GoogleLogin } from 'react-oauth-google';

const Signup = () => {
  const [first_name, setfirst_name] = useState('');
  const [last_name, setlast_name] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const history = useHistory();
  const { signup ,login} = useAuth();

  const handleLoginSuccess = (response) => {
    console.log('Login Successful:', response);
    login(response.tokenId);
    history.push('/dashboard');
  };

  const handleLoginFailure = (response) => {
    console.error('Login Failed:', response);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await fetch('https://learniverse-omega.vercel.app/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ first_name, last_name, email, password }),
      });
      
      const data = await response.json();
      
      if (response.ok) {
        console.log('Signup Successful:', data);
        login(data.token); // Assume your API returns a token upon successful signup
        history.push('/dashboard');
      } else {
        console.error('Signup Failed:', data);
        setErrorMessage(data.message || 'Signup failed. Please try again.');
      }
    } catch (error) {
      console.error('Error:', error);
      setErrorMessage('An error occurred. Please try again.');
    }
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
          {errorMessage && (
            <div className="mt-4 text-red-600 bg-red-100 border border-red-400 p-2 rounded">
              {errorMessage}
            </div>
          )}
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
              <label htmlFor="first_name" className="block mb-2 text-sm font-medium text-gray-600">Full Name</label>
              <input
                id="first_name"
                type="text"
                value={first_name}
                onChange={(e) => setfirst_name(e.target.value)}
                className="block w-full px-4 py-2 mt-2 text-gray-700 bg-white border rounded-md focus:border-blue-500 focus:ring-blue-500 focus:outline-none focus:ring focus:ring-opacity-40"
                placeholder="Enter full name"
              />
            </div>

            <div className="mt-4">
              <label htmlFor="last_name" className="block mb-2 text-sm font-medium text-gray-600">last_name</label>
              <input
                id="last_name"
                type="text"
                value={last_name}
                onChange={(e) => setlast_name(e.target.value)}
                className="block w-full px-4 py-2 mt-2 text-gray-700 bg-white border rounded-md focus:border-blue-500 focus:ring-blue-500 focus:outline-none focus:ring focus:ring-opacity-40"
                placeholder="Enter last_name"
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
            <Link to="/login" className="text-xs text-blue-500 uppercase hover:underline">already have an account? LOGIN</Link>
            <span className="w-1/5 border-b lg:w-1/4"></span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Signup;

