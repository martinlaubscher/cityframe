import React, { useState } from "react";
import "./UserSearchMenuCSS.css";
import Datetime from "react-datetime";
import "react-datetime/css/react-datetime.css";
import moment from "moment-timezone";

const TimeButton = () => {
  const [showOptions, setShowOptions] = useState(true);
  const [datetime, setDatetime] = useState(moment().tz("America/New_York"));

  const handleButtonClick = () => {
    setShowOptions(!showOptions);
  };

  const handleDateTimeChange = (newDateTime) => {
    setDatetime(newDateTime);
  };

  const isValidDate = (current) => {
    const yesterday = moment().tz("America/New_York").subtract(1, "day");
    const inSixteenDays = moment().tz("America/New_York").add(16, "days");
    return current.isAfter(yesterday) && current.isBefore(inSixteenDays);
  };

  return (
    <div>
      {!showOptions && (
        <button
          type="button"
          className="btn btn-primary btn-lg btn-block"
          onClick={handleButtonClick}
        >
          Time
        </button>
      )}
      {showOptions && (
        <div className="option-container">
          <div className="option-label">  
          Time
          </div>
          <div className="option-list">
            <Datetime
              className="dateTimePicker"
              value={datetime}
              onChange={handleDateTimeChange}
              closeOnSelect
              timeFormat="HH:00"
              dateFormat="DD/MM/YYYY"
              isValidDate={isValidDate}
              inputProps={{ readOnly: true }}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default TimeButton;
