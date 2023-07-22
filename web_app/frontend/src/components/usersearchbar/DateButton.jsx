// disabled this component for now, because user can select date in time

import "./UserSearchMenuCSS.css";
import React, { useState } from "react";

const DateButton = () => {
  const [showOptions, setShowOptions] = useState(true);

  const handleButtonClick = () => {
    setShowOptions(true);
  };

  const handleDateTimeChange = (newDateTime) => {
    setDatetime(newDateTime);
    onChange('datetime', newDateTime);
  };

  return (
    <div>
      {!showOptions && (
        <button
          type="button" 
          className="btn btn-primary btn-lg btn-block"
          onClick={handleButtonClick}
        >
          Date
        </button>
      )}
      {showOptions && (
        <div className="option-list">
          Date
          <input type="date" className="date-input" />
        </div>
      )}
    </div>
  );
};

export default DateButton;
