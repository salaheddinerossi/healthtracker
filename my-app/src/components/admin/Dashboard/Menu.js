import React , {useEffect,useState} from 'react';
import { Link ,Outlet} from "react-router-dom";
import "./stylePage1.css";
import useSound from 'use-sound';

  
  



const Menu = () => {

  const [play] = useSound('/sound.wav');  // Change this to the path of your sound file
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
      const eventSource = new EventSource('http://20.216.154.100:8000/unread-count');

      eventSource.onmessage = function(event) {
        const data = JSON.parse(event.data);
        if(data.unread_count > unreadCount) {
          play();
        }
        setUnreadCount(data.unread_count);
  };

      return () => {
          eventSource.close();
      };
  }, [unreadCount, play]);


  return (
    <div className="menu">
          <div className="dashboard">Dashboard
          </div>
          <div className="rectangle_menu" />
          <div className=" form2">
            <div className="form3"> 
             <img className="icon" alt="user_management" src="user_management_icon.png" />
            </div>
            <div>
              <Link className='simple-text' to="/Page1">User Management</Link>
            </div>
         </div>
          <div className=" form2"> 
            <div><img className="icon" alt="Notification" src="notifications_icon.png" /></div>
            <div><Link className='simple-text' to="/Page2">Notifications</Link></div>
            {unreadCount>0 && <div className='notif-cicle'>
              {unreadCount}
            </div>}
          </div>

          <div className=" form2">
            <div><img className="icon" alt="statistics" src="statistics_icon.png" /></div>
            <div>  <Link className='simple-text' to="/Page3">Statistics</Link></div></div>
          <Outlet />
         </div>

  );
};

export default Menu;
 