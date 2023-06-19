import React from "react";

const Footer = (props) => {
  return (  
    <div className="rect-container">
      <div className="flexit">
        <img className="img1" alt="Solar health line" src={props.image1} />
        <div>
          <div className="text-wrapper">{props.text1}</div>
          <p className="text-wrapper-0">{props.paragraph1}</p>
        </div>
      </div>
      <div className="flexit">
        <img className="img2" alt="Solar health line" src={props.image2} />
        <div>
          <div className="text-wrapper-1">{props.text2}</div>
          <p className="text-wrapper-3">{props.paragraph2}</p>
        </div>
      </div>
      <div className="flexit">
        <img className="img3" alt="Solar health line" src={props.image3} />
        <div>
          <div className="text-wrapper-2">{props.text3}</div>
          <p className="text-wrapper-4">{props.paragraph3}</p>
        </div>

      </div>
    </div>
  );
}

export default Footer;
