import "./UserSearchMenuCSS.css";
import React, { useState } from "react";

const StyleButton = ({ onChange }) => {
  const [showOptions, setShowOptions] = useState(true);

  const handleButtonClick = () => {
    setShowOptions(true);
  };

  const handleOptionChange = (event) => {
    onChange('style', Number(event.target.value.slice(-1)));
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
        <div className="option-container">
          <div className="option-label">Style</div>
          <div className="option-list">
            <select className="style-select" onChange={handleOptionChange}>
              <option value="style1">Beaux-Arts</option>
              <option value="style2">Art Deco</option>
              <option value="style3">Gothic Revival</option>
              <option value="style4">Modernism</option>
              <option value="style5">Postmodernism</option>
              <option value="style6">Contemporary</option>
              <option value="style7">Renaissance Revival</option>
              <option value="style8">Colonial Revival</option>
              <option value="style9">Art Nouveau</option>
              <option value="style10">Queen Anne</option>
            </select>
          </div>
        </div>
      )}
    </div>
  );
};

export default StyleButton;
