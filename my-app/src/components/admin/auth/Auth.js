import qs from 'qs';
import React, {  useState } from "react";
import { Link, Outlet, useNavigate   } from "react-router-dom";
import "./styleAuth.css";
import axios from "axios";


const Auth = () => {
    const [name, setName] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(null);
    const navigate = useNavigate();
    
    const handleNameChange = (event) => {
        setName(event.target.value);
    };

    const handlePasswordChange = (event) => {
        setPassword(event.target.value);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        const userData = {
          username: name,
          password: password,
        };

        const config = {
          headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
          },
        };

        try {
            const response = await axios.post(
              'http://20.216.154.100:8000/token',
              qs.stringify(userData),
              config
            );

            console.log(response.data);
            localStorage.setItem('token', response.data.access_token);
            localStorage.setItem('tokenType', response.data.token_type);
            navigate('/Page1');

        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <div className="bg-color">
            <div className="Auth">
                <div className="div1">
                    <img className="element" alt="Braclet" src="Braclet.png" />
                </div>
                <form className="overlap-group-wrapper overlap-group" onSubmit={handleSubmit}>
                    <div>
                        <h1 className="health-tracker">
                            <span className="span">Health</span>
                            <span className="text-wrapper-3"> Tracker</span>
                        </h1>
                        <div className="div"> Admin login </div>
                    </div>

                    <div className="div2">
                        <img className="account" alt="Account" src="Account_Icon.png" />
                        <input className="input-name" type="text" placeholder="Enter your name " value={name}
                            onChange={handleNameChange} />
                    </div>

                    <div className="div2">
                        <img className="password" alt="Password" src="Password_Icon.png" />
                        <input className="input-password" type="password" placeholder="Enter your password " value={password}
                            onChange={handlePasswordChange} />
                    </div>

                    <div>
                        <button className="login" type="submit">
                            Login
                        </button>
                        <Outlet />
                    </div>

                </form>
                {error && <p>{error}</p>}
            </div>
        </div>
    );
};
export default Auth;
