import "./UserSearchMenuCSS.css";
import React, {useEffect, useState} from "react";

const typeOptions = {
  1: 'Commercial',
  2: 'Manufacturing',
  3: 'Park',
  4: 'Residential',
};

const TypeButton = ({onChange, clear}) => {

  const [selectedTypeKey, setSelectedTypeKey] = useState("1");

  const handleOptionChange = (event) => {
    const selectedKey = event.target.value;
    setSelectedTypeKey(selectedKey);
    const selectedType = typeOptions[selectedKey];
    onChange("zone_type", selectedType);
  };

  useEffect(() => {
    if (clear) {
      // reset to default key
      setSelectedTypeKey("1");
      // notify parent of change
      onChange("zone_type", typeOptions["1"]);
    }
  }, [clear, onChange]);

  return (
    <div>
      <div className="option-container">
        <div className="label-explanation-container">
          <div className="option-label">zone type</div>
          <div className="option-explanation">
          {/*insert as needed*/}
          </div>
        </div>
        <div className="option-list" id="type-selection">
          <select className="style-select" onChange={handleOptionChange} value={selectedTypeKey}>
            {Object.keys(typeOptions).map((key) => (
              <option key={key} value={key}>
                {typeOptions[key].toLowerCase()}
              </option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
};

export default TypeButton;