import React from "react";
import "./App.css"
import { BrowserRouter as Router, Route, Routes} from "react-router-dom";
import FirstPage from "./components/firstpage/FirstPage"
import SecondPage from "./components/secondpage/SecondPage"
 
function App() {
 
return (
  <Router>
  <Routes>
  <Route path="/" element={<FirstPage />} />
  <Route exact path="/SecondPage/:macAddress" element={<SecondPage />} />
  </Routes>
  </Router>
);
}

export default App; 