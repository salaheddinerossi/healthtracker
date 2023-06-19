import React , {useState , useEffect} from "react";
import "./style2.css";
import Card from "./Card";
import { useParams } from "react-router-dom";
import { w3cwebsocket as W3CWebSocket } from 'websocket';
import VitalSignGraph from './VitalSignGraph';  // Assuming the file is in the same directory
import 'chart.js/auto'
import axios from 'axios';

//import {Chart as ChartJS , CategoryScale,LinearScale,PointElement,registerables } from 'chart.js'
//ChartJS.register(CategoryScale,LinearScale,PointElement,registerables)


const SecondPage = () => {

const [selectedTimePeriod, setSelectedTimePeriod] = useState("5min");
const [data, setData] = useState([]);

  const [averageData, setAverageData] = useState({
    averageBloodPressure: null,
    averageBodyTemperature: null,
    averageHeartBeat: null,
  });

  const { macAddress } = useParams();

  const client = new W3CWebSocket(`ws://20.216.154.100:8000/ws/vitalsigns/average/${macAddress}/${selectedTimePeriod}`);


  useEffect(() => {
    axios.get(`http://20.216.154.100:8000/vitalsigns/average/${macAddress}/${selectedTimePeriod}`)
      .then(response => {
        setAverageData(response.data);
      })
      .catch(error => {
        console.error('Error fetching data: ', error);
        // Handle the error appropriately in your application
      });

      client.onmessage = (message) => {
        const parsedData = JSON.parse(message.data);
        setData(parsedData);
      };

        // Return a cleanup function that closes the WebSocket connection
      return () => {
        client.close();
      };


      console.log(data)
  

      
  }, [selectedTimePeriod]);  

  let averageHeartBeat =  averageData.averageHeartBeat ? averageData.averageHeartBeat.toFixed(2) : null
  let averageBodyTemperature =  averageData.averageBodyTemperature ? averageData.averageBodyTemperature.toFixed(2) : null
  let averageBloodPressure =  averageData.averageBloodPressure ? averageData.averageBloodPressure.toFixed(2) : null


  const labels = data.map(item => new Date(item.time * 1000).toLocaleTimeString());

  console.log(labels)



  return (
    <div className="secondpage">
      <div className="div ">
        <div className="overlap flexit">
          <div className="health-tracker">
            <span className="span">Health</span>
            <span className="text-wrapper-2">&nbsp;</span>
            <span className="text-wrapper-3">Tracker</span>
          </div>

          <div className="overlap-group">
            <div className="text-wrapper-4 rectangle">
            <select 
              className="time-period-list"
              value={selectedTimePeriod}
              onChange={(e) => setSelectedTimePeriod(e.target.value)}>
              <option value="5min">Last 5 Minutes</option>
              <option value="1hour">Last Hour</option>
              <option value="1day">Last day</option>
              <option value="1month">Last Month</option>
            </select>
            </div>
          </div>

          <div className="profile flexit">
            <div className="ellipse " />
              <div >
                <div className="name">Salah Rddine </div>
                <div className="lastname">Rossi</div>
              </div>
          </div>



        </div>
        <div className="flexit-gap">
          <Card bgColor={"#999cee"} image={"/ph_heartbeat.png"} value={averageHeartBeat} mesure={"Heart beat"} />
          <Card bgColor={"#9cef95"} image={"/blood-pressure2.png"} value={averageBloodPressure} mesure={"Blood Pressure"} />
          <Card bgColor={"#f77676"} image={"/thermometer2.png"} value={averageBodyTemperature} mesure={"Body Temperature"} />
        </div>

        <div>
          <VitalSignGraph title="Blood Pressure" labels={labels} data={data.map(item => item.bloodPressure)} />
          <VitalSignGraph title="Body Temperature" labels={labels} data={data.map(item => item.bodyTemperature)} />
          <VitalSignGraph title="Heart Beat" labels={labels} data={data.map(item => item.heartBeat)} />
        </div>
 
      </div>
    </div>
  );
};
export default SecondPage;