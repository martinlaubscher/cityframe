import "./UserSearchMenuCSS.css";
import React, {useEffect, useState} from "react";

const TreeButton = ({onChange, clear}) => {

  const handleOptionChange = (event) => {
    setSelectedValue(event.target.value);
    onChange("tree", Number(event.target.value.slice(-1)));
  };

  const [selectedValue, setSelectedValue] = useState("option1");


  // watch for the clear flag and reset the state
  useEffect(() => {
    if (clear) {
      setSelectedValue("option1");
    }
  }, [clear, onChange]);

  return (
    <div>
      <div className="option-container">
        <div className="label-explanation-container">
          <div className="option-label">trees</div>
          <div className="option-explanation">
            more or less trees
          </div>
        </div>
        <div className="option-list  radio-list" id="tree-selection">
          <div className="form-check form-check-inline">
            <input
              className="form-check-input"
              type="radio"
              name="treeRadioOptions"
              id="inlineRadio1"
              value="option1"
              checked={selectedValue === "option1"}
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
              name="treeRadioOptions"
              id="inlineRadio2"
              value="option2"
              checked={selectedValue === "option2"}
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
              name="treeRadioOptions"
              id="inlineRadio3"
              value="option3"
              checked={selectedValue === "option3"}
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
              name="treeRadioOptions"
              id="inlineRadio4"
              value="option4"
              checked={selectedValue === "option4"}
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
              name="treeRadioOptions"
              id="inlineRadio5"
              value="option5"
              checked={selectedValue === "option5"}
              onChange={handleOptionChange}
            />
            <label className="form-check-label" htmlFor="inlineRadio5">
              5
            </label>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TreeButton;
