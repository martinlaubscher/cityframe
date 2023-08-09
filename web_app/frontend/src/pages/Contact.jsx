import "./navItemsCSS.css";
export default function Contact() {
  return (
    <div className="contact-container">
      <p className="contact-info">
        get in touch with us with any feedback, comments or issues encountered while on the app.
      </p>
      <div className="contact-methods">
        <div className="general-support">
          <h2>general</h2>
          <p>mojo dojo casa house</p>
          <p>or email us at team@cityfra.me</p>
        </div>
        <div className="support">
          <h2>support</h2>
          <p>For questions or help using CITYFRAME,</p>
          <p>contact help@cityfra.me</p>
        </div>
        <div className="press">
          <h2>business</h2>
          <p>send any business inquiries to</p>
          <p>press@cityfra.me</p>
        </div>
      </div>
    </div>
  );
}
