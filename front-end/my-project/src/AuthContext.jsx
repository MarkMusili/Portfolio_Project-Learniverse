import React, { createContext, useState, useContext } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isSignedUp, setIsSignedUp] = useState(false);
  const [user, setUser] = useState(null);
  const [dashboard, setDashboard] = useState(null)

  const fetchUser = async () => {
    try {
      const res = await fetch('https://learniverse-omega.vercel.app/profile', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include',
      });

      if (res.ok) {
        const data = await res.json();
        setUser(data);
        setIsLoggedIn(true);
      } else {
        setUser(null);
        setIsLoggedIn(false);
      }
    } catch (error) {
      console.error('Error fetching User', error);
      setUser(null);
      setIsLoggedIn(false);
    }
  };

  const fetchDashboard = async () => {
    try {
      const res = await fetch('https://learniverse-omega.vercel.app/dashboard', {
        method: 'GET',
        credentials: 'include',
      })

      if (res.ok) {
        const data = await res.json();
        setDashboard(data);
      } else {
        setDashboard(null);
      }
    } catch (error) {
      console.error('Error fetching Dashboard', error);
      setDashboard(null);
    }
  }

  const login = async (sessionId) => {
    await fetchUser(sessionId);
  };

  const logout = async () => {
    try {
      await fetch('https://learniverse-omega.vercel.app/sessions', {
        method: 'DELETE'
      });
    } catch (error) {
      console.error('Error logging out', error)
    } finally {
      setUser(null);
      setIsLoggedIn(false)
    }
  };

  const signup = () => setIsSignedUp(true);

  return (
    <AuthContext.Provider value={{ isLoggedIn, isSignedUp, user, dashboard, login, logout, signup }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);


  
