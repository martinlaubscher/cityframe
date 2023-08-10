import "./navItemsCSS.css";
export default function Contact() {
  return (
    <div className="contact-container">
      <p className="contact-info">
        get in touch with us with any feedback, comments or issues encountered while on the app.
      </p>
      <div className="contact-methods">
        <div className="general-support">
          <h2>general.</h2>
          <a className="mojo" href="javascript:void(0)">mojo dojo casa house </a>
            <p>for general feedback and comments, please email us at <a href="mailto:team@cityfra.me">team@cityfra.me</a></p>
        </div>
        <div className="support">
          <h2>support.</h2>
            <p>for questions or help using CITYFRAME contact our support helpline <a href="mailto:help@cityfra.me">here</a></p>
        </div>
        <div className="press">
          <h2>business.</h2>
            <p>please send any business inquiries to <a href="mailto:press@cityfra.me">our business email</a></p>
        </div>
      </div>
      <br></br>
      <h3>thank you for visiting our app.</h3>
    </div>
  );
}
