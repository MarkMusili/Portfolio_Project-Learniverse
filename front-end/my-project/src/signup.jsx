import React, { useState } from 'react';
import { Link, useHistory } from 'react-router-dom';
import { useAuth } from './AuthContext'; // Ensure correct path
import { GoogleLogin } from 'react-oauth-google';
import { Eye, EyeOff, ArrowLeft } from "lucide-react";

const Signup = () => {
  const [firstName, setfirstName] = useState('');
  const [lastName, setlastName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const history = useHistory();
  const { signup, login } = useAuth();

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

    if (password !== confirmPassword) {
      setErrorMessage("Passwords do not match!");
      return;
    }

    try {
      const response = await fetch('https://learniverse-omega.vercel.app/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ firstName, lastName, email, password }),
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
    <div className="flex items-center justify-center min-h-screen bg-gray-100 py-8">
      <div className='w-full max-w-md absolute top-4 left-4'>
        <Link to='/' className='text-gray-600 hover:text-gray-900'>
          <ArrowLeft size={24} className='hover:scale-110 transition-transform duration-200' />
        </Link>
      </div>
      <div className="w-full max-w-md overflow-hidden bg-white p-8 rounded-lg shadow-lg">
          <h2 className="text-2xl font-semibold text-center text-gray-700">Create Your New Account</h2>
          <p className="text-l text-center text-gray-600 mt-2">Welcome!</p>

          {/* Google Sign-Up Button */}
        <div className='mt-3'>
          <GoogleLogin
            clientId="YOUR_GOOGLE_CLIENT_ID"
            buttonText="Sign in with Google"
            onSuccess={handleLoginSuccess}
            onFailure={handleLoginFailure}
            cookiePolicy={'single_host_origin'}
            className="w-full mt-4 text-gray-600 transition-colors duration-200 transform border rounded-lg hover:bg-gray-50 p-2"
          />
        </div>

          <div className="flex items-center justify-between mt-4">
            <span className="w-1/5 border-b lg:w-1/4"></span>
            <span className="text-xs text-gray-500 uppercase">or sign up with email</span>
            <span className="w-1/5 border-b lg:w-1/4"></span>
          </div>

          <form onSubmit={handleSubmit} className="mt-4">
            <div className="mt-4">
              <label htmlFor="first_name" className="block mb-2 text-sm font-medium text-gray-600">First Name</label>
              <input
                id="first_name"
                type="text"
                value={firstName}
                onChange={(e) => setfirstName(e.target.value)}
                className="block w-full px-4 py-2 mt-2 text-gray-700 bg-white border rounded-md focus:border-blue-500 focus:ring-blue-500 focus:outline-none focus:ring focus:ring-opacity-40"
                placeholder="Enter first name"
                required
              />
            </div>

            <div className="mt-4">
              <label htmlFor="last_name" className="block mb-2 text-sm font-medium text-gray-600">Last Name</label>
              <input
                id="last_name"
                type="text"
                value={lastName}
                onChange={(e) => setlastName(e.target.value)}
                className="block w-full px-4 py-2 mt-2 text-gray-700 bg-white border rounded-md focus:border-blue-500 focus:ring-blue-500 focus:outline-none focus:ring focus:ring-opacity-40"
                placeholder="Enter last name"
                required
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

            <div className="mt-4 relative">
              <label htmlFor="password" className="block mb-2 text-sm font-medium text-gray-600">Password</label>
              <div className='relative'>
                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="block w-full px-4 py-2 pr-10 text-gray-700 bg-white border rounded-md focus:border-blue-500 focus:ring-blue-500 focus:outline-none focus:ring focus:ring-opacity-40"
                  placeholder="Enter password"
                  required
                />
                <button type='button' className='absolute top-1/2 right-3 transform -translate-y-1/2 text-gray-500 hover:text-gray-700' onClick={() => setShowPassword(!showPassword)}>
                  {showPassword ? <EyeOff size={20}/> : <Eye size={20}/>}
                </button>
              </div>
            </div>

            <div className="mt-4 relative">
              <label htmlFor="confirm password" className="block mb-2 text-sm font-medium text-gray-600">Confirm Password</label>
              <div className='relative'>
                <input
                  id="confirm password"
                  type={showConfirmPassword ? "text" : "password"}
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="block w-full px-4 py-2 pr-10 text-gray-700 bg-white border rounded-md focus:border-blue-500 focus:ring-blue-500 focus:outline-none focus:ring focus:ring-opacity-40"
                  placeholder="Confirm password"
                  required
                />
                <button type="button" className="absolute top-1/2 right-3 transform -translate-y-1/2 text-gray-500 hover:text-gray-700" onClick={() => setShowConfirmPassword(!showConfirmPassword)}>
                  {showConfirmPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </button>
              </div>
            </div>

            <div className="mt-8">
              <button type="submit" className="w-full px-4 py-2 tracking-wide text-white transition-colors duration-200 transform bg-blue-700 rounded-md hover:bg-gray-600 focus:outline-none focus:bg-gray-600">
                <div className='hover:scale-110 transition-transform duration-200'>Sign Up</div>   
              </button>
            </div>
          </form>

          <div className="flex items-center justify-between mt-4">
            <span className="w-1/5 border-b lg:w-1/4"></span>
            <span className='text-xs text-gray-600'>
              Already have an account?{"  "} 
              <Link to="/login" className="text-xs text-blue-500 hover:underline">Log In</Link>
            </span>
            <span className="w-1/5 border-b lg:w-1/4"></span>
          </div>

          {errorMessage && (
            <div className="mt-4 text-red-600 bg-red-100 border border-red-400 p-2 rounded">
              {errorMessage}
            </div>
          )}

      </div>
    </div>
  );
};

export default Signup;

