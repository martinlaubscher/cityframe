import"./navItemsCSS.css"
export default function AboutThisWeb() {
  return (
    <div className="about-this-web-container" >
        <div className="section">
            <span className="title">About</span>
            <p>
              Cityframe helps you find the perfect frame for your shot. Whether
              you're a professional filmmaker or an amateur photographer, use
              cityframe to discover Manhattan in ways you never have before.
            </p>
        </div>

        <div className="section">
            <span className="title">How to use</span>

            <div className="subsection">
                <p className="subtitle">Explore Busyness</p>
                <p>
                  Use the slider on the homepage to see current busyness levels in
                  Manhattan city zones.
                </p>
            </div>

            <div className="subsection">
                <p className="subtitle">Search in city zones</p>
                <p>
                    Select search input parameters and get results of the top ten zones
                    in the city which best match your input returned.
                </p>
                <p>
                    Read your search results data carefully. Zones which are returned
                    may not match all your given search values. The accuracy of search
                    results will vary depending on the input given. Unlikely searches,
                    for example, high busyness in the middle of the night, will include
                    results at more suitable times which match your other search
                    parameters.
                </p>
                <h1></h1>
            </div>
        </div>
    </div>
  );
}
