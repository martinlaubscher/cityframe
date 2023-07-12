import "./UserSearchMenuCSS.css";
import React, { useState } from "react";

const TreeButton = () => {
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
          Tree
        </button>
      )}
      {showOptions && (
          <div className="tree-level">
            <div className="form-check form-switch">
              <input className="form-check-input" type="checkbox" role="switch" id="flexSwitchCheckDefault"/>
              <label className="form-check-label" htmlFor="flexSwitchCheckDefault">Tree</label>
            </div>
        </div>
      )}
    </div>
  );
};

export default TreeButton;
