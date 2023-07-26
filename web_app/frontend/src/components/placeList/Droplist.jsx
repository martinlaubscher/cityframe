//import ListItem from "./ListItem.jsx"
import "../searchresult/SearchResultCSS.css"
import "./DroplistCSS.css"

export default function Droplist ({results, searchOptions, hideList}){
        return(
        <div className="droplist">
            <div className="overlay-info">
            <button
          type="button"
          className="btn-close"
          onClick={hideList}></button>
              <div className="info-zone-style-buyness-tree" style={{marginTop: 30 + "px"}}>
                <div className="info-zone-style">
                  <p>{results.rank.zone}</p>
                  <p>{results.rank.style}  {searchOptions.style}  buildings</p>
                </div>
                <div className="info-busyness-tree">
                  <p>BUSYNESS {results.busyness}</p>
                  <p>TREES {results.trees}</p>
                  <p>RANK {results.rank.rank}</p>
                </div>
              </div>
              <div className="info-time">
                <p>{results.rank.dt_iso}</p>
              </div>
            </div>
        </div>
  );
}