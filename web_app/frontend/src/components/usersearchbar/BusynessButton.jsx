import "./UserSearchMenuCSS.css";
import React, { useState } from "react";

const BusynessButton = () => {
  const [showOptions, setShowOptions] = useState(false);

  const handleButtonClick = () => {
    setShowOptions(!showOptions);
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
        <div className="busyness-level">
          <div className="form-check form-check-inline">
            <input
              className="form-check-input"
              type="radio"
              name="inlineRadioOptions"
              id="inlineRadio1"
              value="option1"
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
            />
            <label className="form-check-label" htmlFor="inlineRadio5">
              5
            </label>
          </div>
        </div>
      )}
    </div>
  );
};

export default BusynessButton;
