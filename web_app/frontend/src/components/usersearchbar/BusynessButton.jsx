import "./UserSearchMenuCSS.css";
import React, { useState } from "react";

const BusynessButton = ({ onChange }) => {
  const [showOptions, setShowOptions] = useState(true);
  const handleButtonClick = () => {
    setShowOptions(!showOptions);
  };

  const handleOptionChange = (event) => {
    onChange('busyness', Number(event.target.value.slice(-1)));
  };

  return (
    <div>
      {!showOptions && (
        <button
          type="button"
          className="btn btn-primary btn-lg btn-block"
          onClick={handleButtonClick}
        >
          Busyness
        </button>
      )}
      {showOptions && (
        <div className="option-container">
        <div className="option-label">  
          Buyness
          </div>
          <div className="option-list">
            <div className="form-check form-check-inline">
              <input
                className="form-check-input"
                type="radio"
                name="inlineRadioOptions"
                id="inlineRadio1"
                value="option1"
                onChange={handleOptionChange}
              />
              <label className="form-check-label" htmlFor="inlineRadio1">
                1
              </label>
            </div>
            <div className="form-check form-check-inline">
              <input
                className="form-check-input"
                type="radio"
                name="inlineRadioOptions"
                id="inlineRadio2"
                value="option2"
                onChange={handleOptionChange}
              />
              <label className="form-check-label" htmlFor="inlineRadio2">
                2
              </label>
            </div>
            <div className="form-check form-check-inline">
              <input
                className="form-check-input"
                type="radio"
                name="inlineRadioOptions"
                id="inlineRadio3"
                value="option3"
                onChange={handleOptionChange}
              />
              <label className="form-check-label" htmlFor="inlineRadio3">
                3
              </label>
            </div>
            <div className="form-check form-check-inline">
              <input
                className="form-check-input"
                type="radio"
                name="inlineRadioOptions"
                id="inlineRadio4"
                value="option4"
                onChange={handleOptionChange}
              />
              <label className="form-check-label" htmlFor="inlineRadio4">
                4
              </label>
            </div>
            <div className="form-check form-check-inline">
              <input
                className="form-check-input"
                type="radio"
                name="inlineRadioOptions"
                id="inlineRadio5"
                value="option5"
                onChange={handleOptionChange}
              />
              <label className="form-check-label" htmlFor="inlineRadio5">
                5
              </label>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default BusynessButton;
