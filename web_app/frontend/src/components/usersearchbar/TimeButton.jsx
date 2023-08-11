// TimeButton.jsx
import React, {useEffect, useState} from "react";
import "./UserSearchMenuCSS.css";
import Datetime from "react-datetime";
import "react-datetime/css/react-datetime.css";
import moment from "moment-timezone";

const TimeButton = ({onChange, clear}) => {
  const [datetime, setDatetime] = useState(moment().tz("America/New_York"));

  const handleDateTimeChange = (newDateTime) => {
    if (moment.isMoment(newDateTime)) {
      setDatetime(newDateTime);
      onChange("datetime", newDateTime.format("YYYY-MM-DD HH:mm"));
      // console.log("handleDateTimeChange newDateTime:", newDateTime.format("YYYY-MM-DD HH:mm"));
    }
  };

  const isValidDate = (current) => {
    const yesterday = moment().tz("America/New_York").subtract(1, "day");
    const inFiveteenDays = moment().tz("America/New_York").add(15, "days");
    return current.isAfter(yesterday) && current.isBefore(inFiveteenDays);
  };
  
  // watch for the clear flag and reset the state
  useEffect(() => {
    if (clear) {
      const newDatetime = moment().tz("America/New_York");
      setDatetime(newDatetime);
      onChange("datetime", newDatetime.format("YYYY-MM-DD HH:mm"));
    }
  }, [clear, onChange]);

  return (
    <div>
      <div className="option-container">
        <div className="label-explanation-container">
          <div className="option-label">time</div>
          <div className="option-explanation">
            preferred day and time
          </div>
        </div>
        <div id="time-selection">
          <Datetime
            className="dateTimePicker"
            value={datetime}
            onChange={handleDateTimeChange}
            closeOnSelect
            timeFormat="HH:00"
            dateFormat="YYYY-MM-DD"
            isValidDate={isValidDate}
            inputProps={{readOnly: true}}
          />
        </div>
      </div>
    </div>
  );
};

export default TimeButton;
