import React from "react";
import "./App.css"
import { BrowserRouter as Router, Route, Routes,Navigate} from "react-router-dom";
import FirstPage from "./components/firstpage/FirstPage"
import SecondPage from "./components/secondpage/SecondPage"
import Page1 from "./components/admin/Dashboard/Page1"; 
import Page2 from "./components/admin/Dashboard/Page2"; 
import Page3 from "./components/admin/Dashboard/Page3"; 

import Auth from "./components/admin/auth/Auth";
import LiveAlertsComponent from "./components/admin/Dashboard/LiveAlertsComponent";
 
function App() {
  const isAuthenticated = () => {
    const token = localStorage.getItem('token');
    return token != null;
  }

 
return (
  <Router>
  <Routes>
  <Route path="/" element={<FirstPage />} />
  <Route exact path="/SecondPage/:macAddress" element={<SecondPage />} />
  <Route path="/Page1" element={<Page1 isAuthenticated={isAuthenticated} />} />

  {isAuthenticated() ? (
    <>
    <Route path="/Page2" element={<Page2 />} />
    <Route path="/Page3" element={<Page3 />} />
    <Route path="/admin" element={<Navigate replace to="/Page1" />} />
    </>
  ) : (
    <Route path="/admin" element={<Auth />} />
    
    
  )}
  




  
  </Routes>
  
  </Router>
  
);
}

export default App; 

