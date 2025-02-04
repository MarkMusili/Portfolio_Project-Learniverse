// Login.js
import React, { useState } from 'react';
import { Link, useHistory } from 'react-router-dom';
import { useAuth } from './AuthContext'; // Ensure correct path
import { GoogleLogin } from 'react-oauth-google';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const history = useHistory();
  const { login } = useAuth();


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
      const response = await fetch('https://learniverse-omega.vercel.app/sessions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        console.log('Login Successful:', data);
        login(data.token); // Assume your API returns a token upon successful login
        history.push('/dashboard');
      } else {
        console.error('Login Failed:', data);
        setErrorMessage(data.message || 'Login failed. Please try again.');
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
            src="https://www.esicm.org/wp-content/uploads/2017/06/elearning.png"
            alt="Learniverse"
          />
        </div>
        <div className="relative z-10 w-1/2 p-8">
          <h2 className="text-2xl font-semibold text-center text-gray-700">Learniverse</h2>
          <p className="text-xl text-center text-gray-600">Welcome back!</p>
          {errorMessage && (
            <div className="mt-4 text-red-600 bg-red-100 border border-red-400 p-2 rounded">
              {errorMessage}
            </div>
          )}
          {/* Google Sign-In Button */}
          <GoogleLogin
            clientId="YOUR_GOOGLE_CLIENT_ID"
            buttonText="Sign in with Google"
            onSuccess={handleLoginSuccess}
            onFailure={handleLoginFailure}
            cookiePolicy={'single_host_origin'}
            className="w-full mt-4 text-gray-600 transition-colors duration-200 transform border rounded-lg hover:bg-gray-50 p-2"
          />

          <div className="flex items-center justify-between mt-4">
            <span className="w-1/5 border-b lg:w-1/4"></span>
            <span className="text-xs text-gray-500 uppercase">or login with email</span>
            <span className="w-1/5 border-b lg:w-1/4"></span>
          </div>

          <form onSubmit={handleSubmit} className="mt-4">
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
              <div className="flex justify-between">
                <label htmlFor="password" className="block mb-2 text-sm font-medium text-gray-600">Password</label>
                <a href="#" className="text-xs text-gray-500 hover:underline">Forgot Password?</a>
              </div>

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
                Login
              </button>
            </div>
          </form>

          <div className="flex items-center justify-between mt-4">
            <span className="w-1/5 border-b lg:w-1/4"></span>
            <Link to="/signup" className="text-xs text-blue-500 uppercase hover:underline">or sign up</Link>
            <span className="w-1/5 border-b lg:w-1/4"></span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;



