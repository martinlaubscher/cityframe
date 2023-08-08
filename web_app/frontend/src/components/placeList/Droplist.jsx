//import ListItem from "./ListItem.jsx"
import "../searchresult/SearchResultCSS.css"
import "./DroplistCSS.css"
import { getImageUrlSmallById } from "../searchresult/ResultPictures";

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
              <div className="rank-zone list-head">
                <p className="rank">{results.rank.rank}</p>
                <p className="zone">{results.rank.zone}</p>
              </div>
              <div className="busyness list-param">
                <div className="busyness-left">
                  <p className="busyness-title">busyness</p>
                </div>
                <div className="busyness-right">
                  <p className="level">level: {results.rank.busyness}</p>
                </div>
              </div>
              <div className="tree list-param">
                <div className="tree-left">
                  <p className="tree-title">trees</p>
                </div>
                <div className="tree-right">
                  <p className="level">level: {results.rank.trees}</p>
                </div>
              </div>

              <div className="style list-param">
                <div className="style-left">
                  <p className="style-title">{results.rank.architecture}</p>
                </div>
                <div className="style-right">
                  <p className="level">
                    count: {results.rank.style}
                  </p>
                </div>
              </div>

              <div className="type list-param">
                <div className="type-left">
                  <p className="type-title">type</p>
                </div>
                <div className="type-right">
                  <p className="type-percent">
                    {results.rank.zone_type}
                  </p>
                </div>
              </div>

              <div className="color-pallete list-param">
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
              <div className="datetime list-param">
                <div className="datetime-left">
                  <p className="datetime-title">date/time</p>
                </div>
                <div className="datetime-right">
                  <p className="level">{results.rank.dt_iso}</p>
                </div>
              </div>

              <div className="pictures list-pic">
                <img className="sample-img"
                  src={getImageUrlSmallById(results.rank.id)}
                  alt={`Image`}
                />
                {/*{console.log(*/}
                {/*  "result.id:",*/}
                {/*  results.rank.id,*/}
                {/*  "url:",*/}
                {/*  getImageUrlSmallById(results.rank.id)*/}
                {/*)}*/}
              </div>
{/*
              <div className="more-info">
                <button className="info-button">more info</button>
              </div>
                */}
            </div>
          </div>          
        </div>
  );
}