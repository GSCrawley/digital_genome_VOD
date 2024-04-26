import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Home from './pages/Home.tsx';
import Player from './pages/Player.tsx';

export default function App() {
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

