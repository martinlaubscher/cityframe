// // StyleButton.jsx
// import "./UserSearchMenuCSS.css";
// import React, { useState } from "react";

// const styleOptions = {
//   1: "Beaux-Arts",
//   2: "Art Deco",
//   3: "Gothic Revival",
//   4: "Modernism",
//   5: "Postmodernism",
//   6: "Contemporary",
//   7: "Renaissance Revival",
//   8: "Colonial Revival",
//   9: "Art Nouveau",
//   10: "Queen Anne",
// };

// const StyleButton = ({ onChange }) => {

//   const handleOptionChange = (event) => {
//     const selectedStyle = styleOptions[Number(event.target.value.slice(-1))];
//     onChange("style", selectedStyle);
//   };

//   return (
//     <div>
//       <div className="option-container">
//         <div className="option-label">Style</div>
//         <div className="option-list">
//           <select className="style-select" onChange={handleOptionChange}>
//             <option value="style1">Beaux-Arts</option>
//             <option value="style2">Art Deco</option>
//             <option value="style3">Gothic Revival</option>
//             <option value="style4">Modernism</option>
//             <option value="style5">Postmodernism</option>
//             <option value="style6">Contemporary</option>
//             <option value="style7">Renaissance Revival</option>
//             <option value="style8">Colonial Revival</option>
//             <option value="style9">Art Nouveau</option>
//             <option value="style10">Queen Anne</option>
//           </select>
//         </div>
//       </div>
//     </div>
//   );
// };

// export default StyleButton;
import "./UserSearchMenuCSS.css";
import React, { useState } from "react";

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

const StyleButton = ({ onChange }) => {
  const handleOptionChange = (event) => {
    const selectedStyle = styleOptions[event.target.value];
    onChange("style", selectedStyle);
  };

  return (
    <div>
      <div className="option-container">
        <div className="option-label">Style</div>
        <div className="option-list">
          <select className="style-select" onChange={handleOptionChange}>
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
