// UserSearchMenu.jsx
import React from "react";
import "./UserSearchMenuCSS.css";
import TimeButton from "./TimeButton";
import DateButton from "./DateButton";
import TreeButton from "./TreeButton";
import BusynessButton from "./BusynessButton";
import StyleButton from "./StyleButton";

const UserSearchMenu = () => {
  return (
    <div className="offcanvas offcanvas-bottom" tabIndex="-1" id="offcanvasBottom" aria-labelledby="offcanvasBottomLabel">
      <div className="button-wrapper-close">
        <button type="button" className="btn-close" data-bs-dismiss="offcanvas" aria-label="Close">
          <svg viewBox="0 0 24 24" fill="#0F0F0F" xmlns="http://www.w3.org/2000/svg">
            <path d="M18.2929 15.2893C18.6834 14.8988 18.6834 14.2656 18.2929 13.8751L13.4007 8.98766C12.6195 8.20726 11.3537 8.20757 10.5729 8.98835L5.68257 13.8787C5.29205 14.2692 5.29205 14.9024 5.68257 15.2929C6.0731 15.6835 6.70626 15.6835 7.09679 15.2929L11.2824 11.1073C11.673 10.7168 12.3061 10.7168 12.6966 11.1073L16.8787 15.2893C17.2692 15.6798 17.9024 15.6798 18.2929 15.2893Z" />
          </svg>
        </button>
      </div>
      <div className="offcanvas-body small">
        <div className="button-container">
          <TimeButton />
          <DateButton />
          <TreeButton />
          <BusynessButton />
          <StyleButton />
        </div>
      </div>
    </div>
  );
};

export default UserSearchMenu;
