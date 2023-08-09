export default function AboutThisWeb() {
  return (
    <div className="about-this-web-container">
      <div className="scrollable-content">
        <div className="section">
          <span className="title">about</span>
          <p>
            CITYFRAME helps you find the perfect frame for your shot. whether
            you're a professional filmmaker or an amateur photographer, use
            cityframe to discover manhattan in ways you never have before.
          </p>
          <br></br>
        </div>

        <div className="section">
          <span className="title">how to use</span>

          <div className="subsection">
            <p className="subtitle">explore busyness</p>
            <p>
              use the slider on the homepage to see current busyness levels in
              manhattan city zones.
            </p>
            <br></br>
          </div>

          <div className="subsection">
            <p className="subtitle">search in city zones</p>
            <p>
              select search input parameters and get results of the top ten zones
              in the city which best match your input returned.
            </p>
            <br></br>
            <p>
              read your search results data carefully. zones which are returned
              may not match all your given search values. the accuracy of search
              results will vary depending on the input given. unlikely searches,
              for example, high busyness in the middle of the night, will include
              results at more suitable times which match your other search
              parameters.
            </p>
            <div style={{ height: '100px' }}> </div>
          </div>
        </div>
      </div>
    </div>
  );
}
