// TimeButton.jsx
import React, { useState } from "react";
import "./UserSearchMenuCSS.css";
import Datetime from "react-datetime";
import "react-datetime/css/react-datetime.css";
import moment from "moment-timezone";

const TimeButton = ({ onChange }) => {
  const [showOptions, setShowOptions] = useState(true);
  const [datetime, setDatetime] = useState(moment().tz("America/New_York"));

  const handleDateTimeChange = (newDateTime) => {
    if (moment.isMoment(newDateTime)) {
      setDatetime(newDateTime);
      onChange("datetime", newDateTime.format("YYYY-MM-DD HH:mm"));
      console.log("handleDateTimeChange newDateTime:", newDateTime.format("YYYY-MM-DD HH:mm"));
    }
  };

  const isValidDate = (current) => {
    const yesterday = moment().tz("America/New_York").subtract(1, "day");
    const inFiveteenDays = moment().tz("America/New_York").add(15, "days");
    return current.isAfter(yesterday) && current.isBefore(inFiveteenDays);
  };

  return (
    <div>
      {showOptions && (
        <div className="option-container">
          <div className="option-label">Time</div>
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
