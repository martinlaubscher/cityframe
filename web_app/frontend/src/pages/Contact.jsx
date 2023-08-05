import "./navItemsCSS.css";
export default function Contact() {
  return (
    <div className="contact-container">
      <p className="contact-info">
        Get in touch with us with any feedback, comments or issues encountered
        while on the app.
      </p>
      <div className="contact-user-input">
        <div className="input-group flex-nowrap email-input">
          <input
            type="text"
            className="form-control"
            placeholder="Your email (optional)"
            aria-label="Email"
            aria-describedby="addon-wrapping"
          />
        </div>
        <div className="input-group flex-nowrap message-input">
          <input
            type="text"
            className="form-control"
            placeholder=" Your message..."
            aria-label="Message"
            aria-describedby="addon-wrapping"
          />
        </div>
      </div>
    </div>
  );
}
