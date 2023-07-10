import React from "react";
const StatisticsCard = (props) => {
     
    return(
        <div className="flexit-page3 card" >
            <div>
                <p className="value">{props.value}</p>
                <p className="mesure">{props.mesure}</p>
            </div>
            <img className="img" src={props.image} />
        </div>
    )
}
export default StatisticsCard;
