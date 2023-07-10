import React , {useState,useEffect} from "react";
import "./stylePage3.css";
import Menu from "./Menu";
import Header from "./Header";
import LiveAlertsComponent from "./LiveAlertsComponent";
import Card from "./Card";
import axios from "axios";
import BarChartComponent from "./BarChartComponent ";
import 'chart.js/auto'
import PieChartComponent from "./PieChartComponent";


const Page3 = () => {
  const [Statistics ,setStatistics] = useState([])
  useEffect(() => {
    axios.get("http://20.216.154.100:8000/stats").catch((err) => {
      console.log(err);
    }).then((res) => {
      setStatistics(res.data)
    })
  }, [])
  console.log(Statistics)
  const colors = ['rgba(54, 162, 235, 0.2)', 'rgba(54, 162, 235, 0.2)'];
  const colors1 = ['rgba(156, 239, 149, 0.2)', 'rgba(156, 239, 149, 0.2)'];
  const colors2 = ['rgba(54, 162, 235, 0.2)', 'rgba(156, 239, 149, 0.2)'];


  return (
    <div className="Page3">
      <LiveAlertsComponent/>
      <div className="div-page1">
        <Menu/>
        <div className="overlap">
           <Header/>
           <div className="title-container">
              <h2 className="title">Statistics</h2>
           </div>
           
           <div className="flexit-gap2">
            {Statistics && Statistics.alert_types_count && <Card bgColor={"#999cee"} image={"/ph_heartbeat.png"} value={Statistics.alert_types_count["Abnormal heart beat"]} mesure={"Heart beat Alerts"} />}
            {Statistics && Statistics.alert_types_count &&<Card bgColor={"#9cef95"} image={"/blood-pressure2.png"} value={Statistics.alert_types_count["Abnormal blood pressure"]} mesure={" Pressure Alerts"} />}
            {Statistics && Statistics.alert_types_count &&<Card bgColor={"#f77676"} image={"/thermometer2.png"} value={Statistics.alert_types_count["High temperature"]} mesure={" Temperature Alerts"} />}
          </div>

          <div>
            <BarChartComponent h1={"number of alerts by age"} data={Statistics.age_groups_alerts} colors={colors} title={"number of alerts / age"} />
            <BarChartComponent h1={"number clients by age"} data={Statistics.age_groups_result} colors={colors1} title={"client/age"} />

          </div>
          <div className="title-container">
              <h2 className="title">Database Statistics</h2>
           </div>
          <div className="flexit-gap2">
            
            {Statistics && Statistics.stats && <Card bgColor={"#999cee"} image={"/database.png"} value={Statistics.stats.avgObjSize.toFixed(2)} mesure={"avgObjSize"} />}
            {Statistics && Statistics.stats &&<Card bgColor={"#9cef95"} image={"/indexes_number.png"} value={Statistics.stats.indexes} mesure={" indexes numbers"} />}
            {Statistics && Statistics.stats &&<Card bgColor={"#f77676"} image={"/indexs.png"} value={(Statistics.stats.indexSize/1000).toFixed(0) +' mb'} mesure={" indexSize"} />}
          </div>
          <div className="pie">
            {Statistics && Statistics.stats &&<PieChartComponent  h1={"usage of database by pourcentage"} dataSize={((Statistics.stats.dataSize-Statistics.stats.storageSize)/1000).toFixed(0)} storageSize={((Statistics.stats.storageSize)/1000).toFixed(0)} colors={colors2} title={"number of alerts / age"} />}

          </div>

          
        </div>
     </div>
   </div>
  );
};
export default Page3;
