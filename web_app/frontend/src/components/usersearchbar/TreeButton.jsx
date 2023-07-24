import "./UserSearchMenuCSS.css";
import React, { useState } from "react";

const TreeButton = ({ onChange }) => {

  const handleOptionChange = (event) => {
    onChange("tree", event.target.checked ? 1 : 0);
  };

  return (
    <div>
      <div className="option-container">
        <div className="option-label">Tree</div>
        <div className="option-list">
          <div className="form-check form-switch">
            <input
              className="form-check-input"
              type="checkbox"
              role="switch"
              id="flexSwitchCheckDefault"
              onChange={handleOptionChange}
            />
            <label
              className="form-check-label"
              htmlFor="flexSwitchCheckDefault"
            ></label>
          </div>
        </div>
      </div>
      {/* )} */}
    </div>
  );
};

export default TreeButton;
