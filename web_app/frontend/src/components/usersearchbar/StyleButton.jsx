import "./UserSearchMenuCSS.css";
import React, { useState } from "react";

const StyleButton = () => {
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
          Style
        </button>
      )}
      {showOptions && (
        <div className="option-list">
          <select>
            <option value="style1">1</option>
            <option value="style2">2</option>
            <option value="style3">3</option>
          </select>
        </div>
      )}
    </div>
  );
};

export default StyleButton;
