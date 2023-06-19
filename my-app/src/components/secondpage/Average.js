import React from "react";

const Averaje = (props) => {
  const { heartBeat, temperature, bloodPressure } = props;

  return (
    <>
      <div className="overlap-2">
        <div className="overlap-3">
          <div className="text-wrapper-5">{heartBeat}</div>
          <div className="text-wrapper-6">Heart beat</div>
        </div>
        <img className="img" alt="Ph heartbeat" src="/ph_heartbeat.png" />
      </div>

      <div className="overlap-4">
        <div className="overlap-5">
          <h1 className="text-wrapper-7">{temperature}</h1>
          <div className="text-wrapper-8">Body Temperature</div>
        </div>
        <img className="img2" alt="temperature" src="/thermometer2.png" />
      </div>

      <div className="overlap-6">
        <div className="overlap-7">
          <div className="text-wrapper-9">{bloodPressure}</div>
          <div className="text-wrapper-10">Blood Pressure</div>
        </div>
        <img className="img3" alt="blood pressure" src="/blood-pressure2.png" />
      </div>
    </>
  );
};

export default Averaje;
