import React from "react";
import "./stylePage1.css";
import { Link } from "react-router-dom";

const Actions = (props) => {

  return (
        <>
        <div className="flex" >
          <div className="fullname">{props.fullname}</div>
          <div className="addressmac">{props.addressmac}</div>
          <div className="address">{props.address}</div>
          <div className="age">{props.age}</div>
          <div className="phone">{props.phone}</div> 
          <div className="flex1">
            <button className="image-button" >
            <Link to={`/SecondPage/${props.addressmac}`}>
              <img className="view" alt="view" src={props.viewIcon} />
          </Link>
                
            </button>
            <button className="image-button" onClick={() => props.handelUpdate(props.id)}>
                 <img className="edit" alt="edit" src={props.editIcon} />
            </button>
            <button className="image-button" onClick={()=> props.handleDelete(props.id)} >
                 <img className="remove" alt="remove" src={props.removeIcon} />
           </button>
           
          </div>
        </div>
       </>
  );
};
export default Actions;
