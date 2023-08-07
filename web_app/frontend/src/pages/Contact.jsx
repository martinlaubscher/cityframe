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
          <p>Email: team@cityfra.me</p>
        </div>
        <div className="support">
          <h2>Support</h2>
          <p>For questions or help using Cityframe:</p>
          <p>Email: help@cityfra.me</p>
        </div>
      </div>
    </div>
  );
}
