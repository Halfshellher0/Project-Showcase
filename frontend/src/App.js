import './App.css';
import React, { Component } from 'react';
import {BrowserRouter as Router} from 'react-router-dom';
import axios from 'axios';
import Navbar from './components/Navbar';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/'
})

class App extends Component {

  state = {
    projects: []
  }

  componentDidMount() {
    api.get('projects')
      .then(res => {
        this.setState({ projects: res.data })
      })
  }

  render() {
    return (
      <Router>
        <Navbar />
        {this.state.projects.map(project => <h2 key={project.id}>{project.name}</h2>)}     
      </Router>
    )      
  }

}

export default App;
