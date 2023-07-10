import React from "react";
const Card = (props) => {
    const cardStyle = {
        backgroundColor: props.bgColor,
        // add other styles as needed
      };
    
    return(
        <div style={cardStyle} className="flexit card" >
            <div>
                <p className="value">{props.value}</p>
                <p className="mesure">{props.mesure}</p>
            </div>
            <img className="img"  src={props.image} />
        </div>
    )
}

export default Card;