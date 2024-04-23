import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Home from './pages/Home';
// import AboutUs from './pages/AboutUs';
import Player from './pages/Player';

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={Home} />
        {/* <Route path="/about-us" component={AboutUs} /> */}
        <Route path="/player/:id" component={Player} />
      </Switch>
    </Router>
  );
}

export default App;