import "./navItemsCSS.css";
export default function Contact() {
  return (
    <div className="contact-container">
      <p className="contact-info">
        Get in touch with us with any feedback, comments or issues encountered while on the app.
      </p>
      <div className="contact-methods">
        <div className="general-support">
          <h2>General Support</h2>
          <p>Mojo Dojo Casa House</p>
          <p>or email us at team@cityfra.me</p>
        </div>
        <div className="support">
          <h2>Support</h2>
          <p>For questions or help using Cityframe,</p>
          <p>contact help@cityfra.me</p>
        </div>
        <div className="press">
          <h2>Press</h2>
          <p>Send any press inquiries to</p>
          <p>press@cityfra.me</p>
        </div>
      </div>
    </div>
  );
}
