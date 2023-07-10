import React from "react";
import "./stylePage1.css";

const Notifications = (props) => {
  const { notificationTitle, notificationContent, isTrue } = props;

const unixTimestamp =props.timestamp ; // Replace this with your timestamp
const date = new Date(unixTimestamp * 1000);
const humanReadableDate = date.toLocaleString(); // Converts Date object to a string using locale conventions


  return (
  
    <div className={`form `}>
      <div className={`form1 ${props.isTrue ? '' : ' isTrue'}`}>
        <p className="notificationtitle">{props.notificationTitle}</p>
        <p className="notificationcontent">{props.notificationTitle} the value is {props.value}, from {props.firstName} {props.lastName} at {humanReadableDate}</p>
      </div> 
   </div>

  );
};

export default Notifications;


