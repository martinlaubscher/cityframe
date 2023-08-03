import React from "react";

export default function ToggleViewButton({ isSearched, viewMode, toggleViewMode }) {
  return (
    <button
      className="btn btn-secondary btn-sm"
      id="toggle-view-button"
      onClick={toggleViewMode}
      disabled={!isSearched}
    >
      {/*if current busyness is showing, display button to switch to results view and vice versa*/}
      {viewMode === 'heatmap' ? 'show search results' : 'show current busyness'}
    </button>
  );
}