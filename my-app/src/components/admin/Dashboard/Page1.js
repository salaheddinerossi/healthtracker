import React ,  { useEffect, useState } from "react";
import "./stylePage1.css";
import Actions from "./Actions";
import FormComponent from "./FormComponent";
import Menu from "./Menu";
import Header from "./Header";
import axios from "axios";
import LiveAlertsComponent from "./LiveAlertsComponent";
import { useNavigate } from "react-router-dom";
  
const Page1 = () => {
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    macAddress: "",
    age: "",
    address: "",
    phone: "",
  });

  const[isUpdate,setIsUpdate]=useState(false);
  const[updateId,setUpdateId]=useState(null);
  const [dataChanged, setDataChanged] = useState(false);


  const isAuthenticated = () => {
    const token = localStorage.getItem('token');
    return token != null;
  }
  const navigate = useNavigate();



  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log("hi");
  
    const token = localStorage.getItem('token');
    const tokenType = localStorage.getItem('tokenType');
  
    const config = {
      headers: {
        'Authorization': `${tokenType} ${token}`,
        'Content-Type': 'application/json',
      },
    };
  
    try {
        let response;

      if(isUpdate){
         response = await axios.put(`http://20.216.154.100:8000/clients/${updateId}`, formData, config);
      }else{
         response = await axios.post("http://20.216.154.100:8000/clients", formData, config);
      }

      setDataChanged(true);
      
      console.log(response.data);
      // Clear form or handle successful form submission
    } catch (err) {
      console.log(err);
      // Handle error during form submission
    }
  };
  
  const handelUpdate = (id) => {
    const token = localStorage.getItem('token');
    const tokenType = localStorage.getItem('tokenType');
    axios.get(`http://20.216.154.100:8000/clients/${id}`, {
      headers: {
        'Authorization': `${tokenType} ${token}`
      }
    })
    .then((response) => {
      setFormData(response.data);
      setIsUpdate(true);
      setUpdateId(id);
    })
    .catch((error) => {
      console.error("There was an error!", error);
    });

    setUpdateId(id);
    setIsUpdate(true);
  }

  const handelCancel = () => {
    setIsUpdate(false);
    setFormData({
      firstName: "",
      macAddress:"",
      age: "",
      address: "",
      phone: "",
      lastName: "",
    });
  }

  const handleDelete = (id) => {
    console.log(id);
    const token = localStorage.getItem('token');
    const tokenType = localStorage.getItem('tokenType');
    axios.delete(`http://20.216.154.100:8000/clients/${id}`, {
      headers: {
        'Authorization': `${tokenType} ${token}`
      },
    })
    .then((response) => {
      setDataChanged(true);
    }
    )
    .catch((error) => {
      console.error("There was an error!", error);
    }
    );

  }

  //get all users
  const [clients, setClients] = useState([]);

  useEffect(() => {

    if(!isAuthenticated()){
      navigate('/admin');
    }
  
    const token = localStorage.getItem('token');
    const tokenType = localStorage.getItem('tokenType');

    const config = {
      headers: {
        'Authorization': `${tokenType} ${token}`
      },
    };

    axios
      .get("http://20.216.154.100:8000/clients", config)
      .then((response) => {
        setClients(response.data);
        setDataChanged(false);
        setFormData({
          firstName: "",
          macAddress:"",
          age: "",
          address: "",
          phone: "",
          lastName: "",
        });
        setIsUpdate(false);
    
      })
      .catch((error) => {
        console.error("There was an error!", error);
      });
    }, [dataChanged]);


  

  return (
    <div className="Page1">
      <LiveAlertsComponent />
      <div className="div-page1">
        <Menu />
        <div className="overlap">
           <Header/>
          
            <div className="flex-center" >
               <FormComponent
                 firstName={formData.firstName}
                 lastName={formData.lastName}
                 macAddress={formData.macAddress}
                 age={formData.age}
                 address={formData.address}
                 phone={formData.phone}
                 handleChange={handleChange}
                 handleSubmit={handleSubmit}
                 handelCancel={handelCancel}
                 isUpdate={isUpdate} />
            </div>

           <div className="title-container">
              <h2 className="title">Users and actions</h2>
           </div>

           <div className="flexit-gap "> 
             <div className="w-80">
                <div className="flex">
                 <div>First and Last name</div>
                 <div>Mac Address</div>
                 <div>Address</div>
                 <div>Age</div>
                 <div>Phone</div>
                 <div>Actions</div>
             </div>
             {clients.map((client, index) => {
              return (
                <Actions 
                  key={index}
                  fullname={client.firstName + ' ' + client.lastName}
                  addressmac={client.macAddress}
                  address={client.address}
                  age={client.age}
                  phone={client.phone}
                  viewIcon="view_icon.png" 
                  editIcon="edit_icon.png" 
                  removeIcon="  remove_icon.png"
                  id={client.id}
                  handelUpdate={handelUpdate}
                  handleDelete={handleDelete}

                />
               )})
              }

           </div>

           </div>
  
        </div>

      </div>
   </div>
  );
};
export default Page1;
