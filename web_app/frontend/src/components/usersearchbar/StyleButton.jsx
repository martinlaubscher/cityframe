import "./UserSearchMenuCSS.css";
import React, {useEffect, useState} from "react";

const styleOptions = {
  1: 'All',
  2: 'neo-Georgian',
  3: 'Greek Revival',
  4: 'Romanesque Revival',
  5: 'neo-Grec',
  6: 'Renaissance Revival',
  7: 'Beaux-Arts',
  8: 'Queen Anne',
  9: 'Italianate',
  10: 'Federal',
  11: 'neo-Renaissance'
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
          <div className="option-label">Style</div>
          <div className="option-explanation">
            architecture
          </div>
        </div>
        <div className="option-list" id="style-selection">
          <select className="style-select" onChange={handleOptionChange} value={selectedStyleKey}>
            {Object.keys(styleOptions).map((key) => (
              <option key={key} value={key}>
                {styleOptions[key]}
              </option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
};

export default StyleButton;
