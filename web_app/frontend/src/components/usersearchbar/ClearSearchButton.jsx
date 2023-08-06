import React from 'react';

const ClearSearchButton = ({clearSearchOptions}) => {
  return (
    <button type="button"
            className="btn btn-secondary btn-sm"
            id="clear-search-button"
            onClick={clearSearchOptions}>
      clear search
    </button>
  );
};

export default ClearSearchButton;