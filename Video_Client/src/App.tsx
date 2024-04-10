import React from 'react';
import logo from './assets/logo.svg';
import Home from './pages/Home';
import LKUINavButton from './components/LKUINavButton';
import { Home24Regular, Home24Filled, Info24Regular, Info24Filled } from '@fluentui/react-icons';
import AboutUs from './pages/AboutUs';
import './assets/fonts/typonine-legacy/typonine.css'
import './assets/fonts/jotia.css'
import './assets/fonts/mark-pro/markpro.css'
import { BrowserRouter as Router, Route, Switch, Link } from 'react-router-dom';
import './style/App.css';
import Player from './pages/Player';

const ConditionalStuff: React.FC<{}> = (): React.ReactElement | null => {
  if (window.location.href.includes('lookeeloo-canary')) {
    document.title = 'Lookeeloo (Canary [BETA])'
    return (
      <div className='lkui-on-canary'>
        <p>Lookeeloo Canary Channel. Errors will be automatically alerted. Additional bugs may be reported to <Link to='mailto:zeanfender11@gmail.com'>zeanfender11@gmail.com</Link> or <Link to='mailto:arsyadyudhistira2@gmail.com'>arsyadyudhistira2@gmail.com</Link></p>
      </div>
    )
  } else if (window.location.href.includes('localhost')) {
    document.title = 'Lookeeloo (running at localhost)'
    return (
      <div className='lkui-on-canary'>
        <p>Lookeeloo (running at <code>localhost</code>.) Check console for further messages</p>
      </div>
    )
  } else {
    return null;
  }
}

function App() {
  return (
    <div className="lkui-main">
      <Router>
        <div className='lkui-header'>
          <Link to='/'>
            <img src={logo} width={150} alt='Lookeeloo logo'></img>
          </Link>
          <LKUINavButton path='/' regComponent={Home24Regular} filledComponent={Home24Filled} />
          <LKUINavButton path='/about-us' regComponent={Info24Regular} filledComponent={Info24Filled} />
          <ConditionalStuff />
        </div>
        <div className='lkui-App'>
          <Switch>
            <Route exact path='/' component={Home}></Route>
            <Route path='/about-us' component={AboutUs}></Route>
            <Route path='/player/:id' component={Player}></Route>
          </Switch>
        </div>
      </Router>
    </div>
  );
}

export default App;
