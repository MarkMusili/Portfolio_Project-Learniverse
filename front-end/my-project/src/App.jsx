import React from 'react';
import { BrowserRouter as Router, Route,  Switch, Redirect, useLocation } from 'react-router-dom';
import { GoogleOAuthProvider } from 'react-oauth-google';
import { motion, AnimatePresence } from 'framer-motion';
import LandingPage from './Landingpage';
import Dashboard from './Dashboard';
import Roadmap from './Roadmap';
import ChatComponent from './chat';
import Sidebar from './Sidebar';
import Header from './Header';
import Calendar2024 from './Calendar';
import Login from './login';
import Signup from './signup';
import Profile from './profile';
import {AuthProvider, useAuth } from './AuthContext';
// import { Component } from 'lucide-react';

const pageVariants = {
  initial: { opacity: 0 },
  animate: { opacity: 1 },
  exit: { opacity: 0 }
};

const PublicRoute = ({ component: Component, ...rest }) => (
  <Route 
    {...rest}
    render={(props) => (
      <motion.div initial="initial" animate="animate" exit="exit" variants={pageVariants} transition={{ duration: 0.5 }}>
        <Component {...props} />
      </motion.div>
    )}
  />
)

// ProtectedRoute component to handle redirection
const ProtectedRoute = ({ component: Component, ...rest }) => {
  const { isLoggedIn } = useAuth();

  return (
    <Route
      {...rest}
      render={(props) =>
        isLoggedIn ? (
          <motion.div initial="initial" animate="animate" exit="exit" variants={pageVariants} transition={{ duration: 0.3 }}>
            <Component {...props} />
          </motion.div>
        ) : (
          <Redirect to="/login" />
        )
      }
    />
  );
};

// Layout component with Sidebar and Header
const Layout = ({ children }) => (
  <div className="flex h-screen">
    <Sidebar />
    <div className="flex flex-col w-full">
      <Header />
      {children}
    </div>
  </div>
);

const AnimatedRoutes = () => {
  const location = useLocation();

  return (
    <AnimatePresence mode='wait'>
      <Switch location={location} key={location.pathname}>
        {/* Public routes */}
        <PublicRoute exact path="/" component={LandingPage} />
        <PublicRoute path="/signup" component={Signup} />
        <PublicRoute path="/login" component={Login} />

        <Route>
          <Layout>
            <Switch location={location} key={location.pathname}>
              {/* Protected Routes */}
              <ProtectedRoute path="/profile" component={Profile} />
              <ProtectedRoute path="/dashboard" component={Dashboard} />
              <ProtectedRoute path="/chats" component={ChatComponent} />
              <ProtectedRoute path="/roadmap" component={Roadmap} />
              <ProtectedRoute path="/calendar" component={Calendar2024} />

              {/* Catch-all route */}
              <Redirect to="/" />
            </Switch>
          </Layout>
        </Route>
      </Switch>
    </AnimatePresence>
  )
}

const App = () => (
  <div className='bg-blue-50'>
    <Router>
      <AuthProvider>
        <GoogleOAuthProvider clientId="YOUR_GOOGLE_CLIENT_ID">
          <AnimatedRoutes />
        </GoogleOAuthProvider>
      </AuthProvider>
    </Router>
  </div>
);

export default App;