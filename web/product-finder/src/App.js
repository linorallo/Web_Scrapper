import React from 'react';
//import './Assets/css/default.min.css';
import Header from './components/headerComponents/header';
import Footer from './components/footerComponent/footer';
import Homepage from './components/pages/homePage';

function App() {
  return (
    <div className="App">
      <Header/>
      <Homepage/>
      <Footer/>
    </div>
  );
}

export default App;
