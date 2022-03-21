
   
import React, { useEffect, useState } from "react";
import './clock.css'
function Zegar() {
  const [clockState, setClockState] = useState();

  useEffect(() => {
    setInterval(() => {
      const date = new Date();
      setClockState(date.toLocaleTimeString());
    }, 1000);
  }, []);

  return(
    <div>
      <div class = 'zegar-diw' 
             style={{ fontSize: "65px", margin: "60px" }}>{clockState}
            
        </div>
    </div>
        );
}

export default Zegar;