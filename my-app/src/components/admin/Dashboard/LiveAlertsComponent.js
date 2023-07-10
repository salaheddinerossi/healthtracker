import React, { useEffect, useState } from 'react';
import { w3cwebsocket as W3CWebSocket } from 'websocket';
import './Alerts.css';  // Import the CSS file

const LiveAlertsComponent = () => {
    const [alerts, setAlerts] = useState([]);

    useEffect(() => {
        const client = new W3CWebSocket('ws://20.216.154.100:8000/alertos');

        client.onopen = () => {
            console.log('WebSocket Client Connected');
    
            // Send ping every 5 seconds
            setInterval(() => {
                if (client.readyState === WebSocket.OPEN) {
                    client.send('ping');
                }
            }, 5000);
        };
        
        client.onmessage = (message) => {
            const dataFromServer = JSON.parse(message.data);
            console.log('got reply! ', dataFromServer);
            if (dataFromServer.type === 'vital_signs_alert') {
                setAlerts((oldArray) => [dataFromServer, ...oldArray]);  // Add new alert at the beginning of the array
                setTimeout(() => {
                    setAlerts((oldArray) => {
                        const newArray = [...oldArray];
                        newArray.pop(); // remove the oldest alert
                        return newArray;
                    });
                }, 10000); // Alert disappears after 10 seconds
            }
        };
    
        client.onping = () => {
            console.log('Received ping');
        };
    
        client.onpong = () => {
            console.log('Received pong');
        };
    
        // Cleanup function
        return () => {
            if (client.readyState === WebSocket.OPEN || client.readyState === WebSocket.CONNECTING) {
                client.close();
                console.log('WebSocket Client Disconnected');
            }
        };
    }, []);

    return (
        <div>
            <div className="alert-list">
                {alerts.map((alert, index) => (
                    <div key={index} className="alert">
                        <p className='Title-bold'>{alert.alert}</p>
                        <p>{alert.value}</p>
                        <p>{alert.firstName} {alert.lastName}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default LiveAlertsComponent;
