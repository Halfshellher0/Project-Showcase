import './App.css';
import {BrowserRouter as Router} from 'react-router-dom';
import axios from 'axios';
import Navbar from './components/Navbar';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/projects/'
})

function App() {
  constructor() {
    super();
    api.get('/').then(res => {
      console.log(res.data)
    })
  }

  return (
    <Router>
      <Navbar />
    </Router>
  );
}

export default App;
