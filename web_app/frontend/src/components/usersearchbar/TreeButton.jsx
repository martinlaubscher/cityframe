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
            <div class="form-check form-switch">
              <input class="form-check-input" type="checkbox" role="switch" id="flexSwitchCheckDefault"/>
              <label class="form-check-label" for="flexSwitchCheckDefault">Tree</label>
            </div>
        </div>
      )}
    </div>
  );
};

export default TreeButton;
