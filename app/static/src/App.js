import React, { Component } from 'react';
import Search from './Search';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h1 className="App-title">Finn  næringskode:</h1>
          <Search />
        </header>

      </div>
    );
  }
}

export default App;
