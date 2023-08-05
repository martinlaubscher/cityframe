import "./UserSearchMenuCSS.css";
import React, { useState } from "react";

const TreeButton = ({ onChange }) => {
  // const handleOptionChange = (event) => {
  //   onChange("tree", event.target.checked ? 1 : 0);
  // };
  const handleOptionChange = (event) => {
    onChange("tree", Number(event.target.value.slice(-1)));
  };

  // return (
  //   <div>
  //     <div className="option-container">
  //       <div className="option-label">Tree</div>
  //       <div className="option-list">
  //         <div className="form-check form-switch">
  //           <input
  //             className="form-check-input"
  //             type="checkbox"
  //             role="switch"
  //             id="flexSwitchCheckDefault"
  //             onChange={handleOptionChange}
  //           />
  //           <label
  //             className="form-check-label"
  //             htmlFor="flexSwitchCheckDefault"
  //           ></label>
  //         </div>
  //       </div>
  //     </div>
  //   </div>
  // );
  return (
    <div>
      <div className="option-container">
        <div className="option-label">Tree</div>
        <div className="option-list radio-list">
          <div className="form-check form-check-inline">
            <input
              className="form-check-input"
              type="radio"
              name="treeRadioOptions"
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
              name="treeRadioOptions"
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
              name="treeRadioOptions"
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
              name="treeRadioOptions"
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
              name="treeRadioOptions"
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
    </div>
  );
};

export default TreeButton;
