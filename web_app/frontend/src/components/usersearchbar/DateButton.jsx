import "./UserSearchMenuCSS.css";
import React, { useState } from "react";

const DateButton = () => {
  const [showOptions, setShowOptions] = useState(false);

  const handleButtonClick = () => {
    setShowOptions(true);
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
          <input type="date" className="date-input" />
        </div>
      )}
    </div>
  );
};

export default DateButton;
