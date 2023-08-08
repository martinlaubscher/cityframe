import "./UserSearchMenuCSS.css";
import React, {useEffect, useState} from "react";

const styleOptions = {
  1: 'neo-Georgian',
  2: 'Greek Revival',
  3: 'Romanesque Revival',
  4: 'neo-Grec',
  5: 'Renaissance Revival',
  6: 'Beaux-Arts',
  7: 'Queen Anne',
  8: 'Italianate',
  9: 'Federal',
  10: 'neo-Renaissance'
};

const StyleButton = ({onChange, clear}) => {

  const [selectedStyleKey, setSelectedStyleKey] = useState("1");

  const handleOptionChange = (event) => {
    const selectedKey = event.target.value;
    setSelectedStyleKey(selectedKey);
    const selectedStyle = styleOptions[selectedKey];
    onChange("style", selectedStyle);
  };

  useEffect(() => {
    if (clear) {
      // reset to default key
      setSelectedStyleKey("1");
      // notify parent of change
      onChange("style", styleOptions["1"]);
    }
  }, [clear, onChange]);

  return (
    <div>
      <div className="option-container">
        <div className="label-explanation-container">
          <div className="option-label">style</div>
          <div className="option-explanation">
            architecture
          </div>
        </div>
        <div className="option-list" id="style-selection">
          <select className="style-select" onChange={handleOptionChange} value={selectedStyleKey}>
            {Object.keys(styleOptions).map((key) => (
              <option key={key} value={key}>
                {styleOptions[key].toLowerCase()}
              </option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
};

export default StyleButton;
