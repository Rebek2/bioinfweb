
import React from 'react';
import App2 from './components/blog/blog'
import App4 from './components/navbar/navBar'
import Zegar from './components/Addons/Clock'
import './App.css'
function App() 
{
  return (
    <div class = 'App'>
      <App4/>
      <center>
        <Zegar/>
      </center>
    
    </div>
  )
}





export default App;
