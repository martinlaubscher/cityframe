import React, { useState } from "react";
import "./UserSearchMenuCSS.css";

const TimeButton = () => {
  const [showOptions, setShowOptions] = useState(false);
  const [time, setTime] = useState(new Date().toLocaleTimeString("en-US", { timeZone: "America/New_York", hour12: false }));

  const handleButtonClick = () => {
    setShowOptions(true);
  };

  const handleTimeChange = (event) => {
    setTime(event.target.value);
  };

  return (
    <div>
      {!showOptions && (
        <button
          type="button" 
          className="btn btn-primary btn-lg btn-block"
          onClick={handleButtonClick}
        >
          {time}
        </button>
      )}
      {showOptions && (
        <div className="option-list">
          <input
            type="time"
            className="time-input"
            value={time}
            onChange={handleTimeChange}
          />
        </div>
      )}
    </div>
  );
};

export default TimeButton;
