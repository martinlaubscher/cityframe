//import ListItem from "./ListItem.jsx"
import "../searchresult/SearchResultCSS.css"
import "./DroplistCSS.css"

export default function Droplist ({results, searchOptions, hideList}){
        return(
        <div className="droplist">
          <div className="div-button">
          <button
            type="button"
            className="btn-close"
            onClick={hideList}>
          </button> 
        </div>
          <div className="overlay-info">   
            <div className="list-info">
              <div className="rank-zone">
                <p className="rank">{results.rank.rank}</p>
                <p className="zone">{results.rank.zone}</p>
              </div>
              <div className="busyness">
                <div className="busyness-left">
                  <p className="busyness-title">busyness</p>
                </div>
                <div className="busyness-right">
                  <p className="level">level: {results.rank.busyness}</p>
                </div>
              </div>
              <div className="tree">
                <div className="tree-left">
                  <p className="tree-title">trees</p>
                </div>
                <div className="tree-right">
                  <p className="level">level: {results.rank.trees}</p>
                </div>
              </div>

              <div className="style">
                <div className="style-left">
                  <p className="style-title">{searchOptions.style}</p>
                </div>
                <div className="style-right">
                  <p className="level">
                    count: {results.rank.style}
                  </p>
                </div>
                
              </div>
              <div className="color-pallete">
                <div className="color-pallete-left">
                  <p className="colors-title">colors</p>
                </div>
                <div className="color-pallete-right place-pallete">
                  
                  {results.rank.pallete.map((hex, index) => (
                    <div
                      key={index}
                      className="hexdiv"
                      style={{ backgroundColor: hex }}
                    ></div>
                  ))
                  }
                </div>
              </div>
              <div className="datetime">
                <div className="datetime-left">
                  <p className="datetime-title">date/time</p>
                </div>
                <div className="datetime-right">
                  <p className="level">{results.rank.dt_iso}</p>
                </div>
              </div>
              <div className="more-info">
                <button className="info-button">more info</button>
              </div>
            </div>
          </div>          
        </div>
  );
}