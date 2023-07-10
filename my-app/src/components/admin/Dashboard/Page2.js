import React from "react";
import { useState,useEffect } from "react";
import "./stylePage2.css";
import Menu from "./Menu";
import Header from "./Header";
import Notifications from "./Notifications";
import axios from "axios";
import LiveAlertsComponent from "./LiveAlertsComponent";


const Page2 = () => {

  const [oldAlerts, setOldAlerts] = useState([]);

  const markAsRead = () => {
      axios.post('http://20.216.154.100:8000/markasread')
          .catch(error => {
              console.error('There was an error marking alerts as read!', error);
          });
  };

  useEffect(() => {
      // Fetch all alerts from backend
      axios.get('http://20.216.154.100:8000/getalerts')
      .then(response => {
          const sortedAlerts = response.data.sort((a, b) => b.timestamp - a.timestamp);
          setOldAlerts(sortedAlerts);
          console.log(sortedAlerts);

          markAsRead();  // Call the markAsRead function after fetching alerts
      })
      .catch(error => {
          console.error('There was an error fetching alerts!', error);
      });
    }, []);







  return (
    <div className="Page2">
      <LiveAlertsComponent/>
      <div className="div-page1">
         <Menu/> 
        <div className="overlap"> 
          <Header/>
          

          <div className="title-container">
              <h2 className="title">Notifications</h2>
           </div>
          {oldAlerts.map((alert, index) => (
              <Notifications
                  key={index}
                  notificationTitle={alert.alert}
                  value={alert.value}
                  isTrue={alert.isRead}
                  firstName={alert.firstName}
                  lastName={alert.lastName}
                  timestamp={alert.timestamp}
              />
          ))}

       </div > 
      </div>
    </div>
  );
};
export default Page2;
