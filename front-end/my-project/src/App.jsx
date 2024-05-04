import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import LandingPage from './Landingpage';
import Dashboard from './Dashboard';
import Roadmap from './Roadmap';
import ChatComponent from './chat';
import Sidebar from './Sidebar';
import Header from './Header';
import Calendar2024 from './Calendar';

function App() {
  return (
    <div className='bg-blue-50'>
    <Router>
      <Switch>
        {/* Route without Sidebar and Header */}
        <Route exact path="/" component={LandingPage} />

        {/* Routes with Sidebar and Header */}
        <Route>
          <div className="flex h-screen">
            <Sidebar />
            <div className="flex flex-col w-full">
              <Header />
              <Switch>
                <Route path="/dashboard" component={Dashboard} />
                <Route path="/chats" component={ChatComponent} />
                <Route path="/roadmap" component={Roadmap} />
                <Route path="/calendar" component={Calendar2024} />
              </Switch>
            </div>
          </div>
        </Route>
      </Switch>
    </Router>
    </div>
  );
}

export default App;
