import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
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

function App() {
  return (
    <div className='bg-blue-50'>
      <Router>
        <Switch>
          {/* Route without Sidebar and Header */}
          <Route exact path="/" component={LandingPage} />
          <Route path="/profile" Component={Profile} />
          {/* <Route path="/signup" component={Signup} /> */}

          {/* Routes with Sidebar and Header */}
          <Route>
            <GoogleOAuthProvider clientId="YOUR_GOOGLE_CLIENT_ID">
              <div className="flex h-screen">
                <Sidebar />
                <div className="flex flex-col w-full">
                  <Header />
                  <Switch>
                    <Route path="/signup" component={Signup} />
                    <Route path="/profile" Component={Profile} />
                    <Route path="/login" component={Login} />
                    <Route path="/dashboard" component={Dashboard} />
                    <Route path="/chats" component={ChatComponent} />
                    <Route path="/roadmap" component={Roadmap} />
                    <Route path="/calendar" component={Calendar2024} />
                  </Switch>
                </div>
              </div>
            </GoogleOAuthProvider>
          </Route>
        </Switch>
      </Router>
    </div>
  );
}

export default App;
