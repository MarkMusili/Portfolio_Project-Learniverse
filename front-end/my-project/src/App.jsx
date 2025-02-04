import React from 'react';
import { BrowserRouter as Router, Route,  Switch, Redirect } from 'react-router-dom';
import { GoogleOAuthProvider } from 'react-oauth-google';
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



// ProtectedRoute component to handle redirection
const ProtectedRoute = ({ component: Component, ...rest }) => {
  const { isLoggedIn } = useAuth();

  return (
    <Route
      {...rest}
      render={(props) =>
        isLoggedIn ? (
          <Component {...props} />
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

const AppRoutes = () => (
  <Switch>
    {/* Public routes */}
    <Route exact path="/" component={LandingPage} />
    <Route path="/signup" component={Signup} />
    <Route path="/login" component={Login} />

    {/* Protected routes */}
    <ProtectedRoute path="/profile" component={Profile} />
    <ProtectedRoute path="/dashboard" component={Dashboard} />
    <ProtectedRoute path="/chats" component={ChatComponent} />
    <ProtectedRoute path="/roadmap" component={Roadmap} />
    <ProtectedRoute path="/calendar" component={Calendar2024} />

    {/* Catch-all route */}
    <Redirect to="/" />
  </Switch>
);

const App = () => (
  <div className='bg-blue-50'>
    <Router>
      <AuthProvider>
        <GoogleOAuthProvider clientId="YOUR_GOOGLE_CLIENT_ID">
          <Switch>
            <Route path="/" exact>
              <LandingPage />
            </Route>
            <Route>
              <Layout>
                <AppRoutes />
              </Layout>
            </Route>
          </Switch>
        </GoogleOAuthProvider>
      </AuthProvider>
    </Router>
  </div>
);

export default App;