import React from "react";

const FormComponent = (props) => {
  const {
    firstName,
    lastName,
    macAddress,
    age,
    address,
    phone,
    handleChange,
    handleSubmit,
  } = props;

  return (
    <div  className="form">
      <div className="title-container">
        <h2 className="title">{props.isUpdate ? "Update":"Create"} an user</h2>
      </div>
      <div>
        <input
            className=" bg-input"
            type="text"
            name="firstName"
            placeholder="First name" 
            value={firstName}
            onChange={handleChange}
          />
          <input
            className="bg-input"
            type="text"
            name="macAddress"
            placeholder="Mac address" 
            value={macAddress}
            onChange={handleChange}
          />

      </div>
      <div>
        <input
            type="number"
            name="age"
            placeholder="Age" 
            className="bg-input"
            value={age}
            onChange={handleChange}
          />
          <input
            type="text"
            name="address"
            placeholder="Address" 
            className="bg-input"
            value={address}
            onChange={handleChange}
          />
      </div>

      <div>
        <input
            className="bg-input"
            type="text"
            name="phone"
            placeholder="Phone" 
            value={phone}
            onChange={handleChange}
          />
          <input
            className="bg-input"
            type="text"
            name="lastName"
            placeholder="Last name" 
            value={lastName}
            onChange={handleChange}
          />
      </div>
      
      <div className="button-container">
          {props.isUpdate ? <button className="overlap-cancel cancel" onClick={props.handelCancel}>cancel</button> : "" }
          <button className="overlap-submit submit" onClick={(event) => props.handleSubmit(event)}>{props.isUpdate ? "Update" : "Submit"}</button>
      </div>

    </div>
  );
};
export default FormComponent;
