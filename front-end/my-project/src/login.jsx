import React from 'react';
import { GoogleLogin, GoogleOAuthProvider } from 'react-oauth-google';
import { Link } from 'react-router-dom';

const Login = () => {
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

  return (
    <GoogleOAuthProvider clientId="YOUR_GOOGLE_CLIENT_ID">
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

            <form className="mt-4">
              <div className="mt-4">
                <label className="block mb-2 text-sm font-medium text-gray-600">Email Address</label>
                <input
                  className="block w-full px-4 py-2 mt-2 text-gray-700 bg-white border rounded-md focus:border-blue-500 focus:ring-blue-500 focus:outline-none focus:ring focus:ring-opacity-40"
                  type="email"
                  placeholder="Enter email address"
                />
              </div>

              <div className="mt-4">
                <div className="flex justify-between">
                  <label className="block mb-2 text-sm font-medium text-gray-600">Password</label>
                  <a href="#" className="text-xs text-gray-500 hover:underline">Forgot Password?</a>
                </div>

                <input
                  className="block w-full px-4 py-2 mt-2 text-gray-700 bg-white border rounded-md focus:border-blue-500 focus:ring-blue-500 focus:outline-none focus:ring focus:ring-opacity-40"
                  type="password"
                  placeholder="Enter password"
                />
              </div>

              <div className="mt-8">
                <button className="w-full px-4 py-2 tracking-wide text-white transition-colors duration-200 transform bg-blue-700 rounded-md hover:bg-gray-600 focus:outline-none focus:bg-gray-600">
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
    </GoogleOAuthProvider>
  );
};

export default Login;
