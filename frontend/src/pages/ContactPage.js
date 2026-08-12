import React, { useState } from 'react';
import { FaPhone, FaEnvelope, FaMapMarkerAlt, FaWhatsapp, FaPaperPlane } from 'react-icons/fa';
import './ContactPage.css';

export default function ContactPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    message: ''
  });
  const [submitted, setSubmitted] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // In a real app, this would send an API request
    setSubmitted(true);
    setTimeout(() => {
      setSubmitted(false);
      setFormData({ name: '', email: '', phone: '', message: '' });
    }, 4000);
  };

  return (
    <div className="contact-page">
      {/* HERO SECTION */}
      <section className="contact-hero">
        <div className="contact-hero-content">
          <div className="contact-badge">✦ Let's Connect ✦</div>
          <h1>Contact <em>Us</em></h1>
          <p>We are a fresh startup and we love hearing from our community. Get in touch for inquiries, collaborations, or just to say hi!</p>
        </div>
      </section>

      {/* CONTACT CONTENT SECTION */}
      <section className="contact-content-section">
        <div className="contact-grid">
          {/* Contact Form Card */}
          <div className="contact-card form-card">
            <h2>Send Us a Message</h2>
            <p className="card-sub">Fill out the form below and our team will get back to you within 24 hours.</p>

            {submitted ? (
              <div className="form-success-alert">
                <h3>Message Sent Successfully!</h3>
                <p>Thank you for reaching out. We will get back to you shortly.</p>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="contact-form">
                <div className="form-row-two">
                  <div className="form-group">
                    <label>Full Name *</label>
                    <input
                      type="text"
                      name="name"
                      value={formData.name}
                      onChange={handleChange}
                      placeholder="John Doe"
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Email Address *</label>
                    <input
                      type="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      placeholder="john@example.com"
                      required
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label>Phone Number</label>
                  <input
                    type="tel"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    placeholder="+91 9876543210"
                  />
                </div>

                <div className="form-group">
                  <label>Message *</label>
                  <textarea
                    name="message"
                    value={formData.message}
                    onChange={handleChange}
                    placeholder="How can we help you today?"
                    rows="5"
                    required
                  ></textarea>
                </div>

                <button type="submit" className="submit-btn">
                  Send Message <FaPaperPlane size={12} />
                </button>
              </form>
            )}
          </div>

          {/* Contact Info Card */}
          <div className="contact-card info-card">
            <h2>Contact Information</h2>
            <div className="info-list">
              <div className="info-item">
                <div className="info-icon-box"><FaPhone style={{ transform: 'rotate(90deg)' }} /></div>
                <div>
                  <div className="info-label">Phone</div>
                  <div className="info-val">+91 9104139899</div>
                </div>
              </div>

              <div className="info-item">
                <div className="info-icon-box"><FaEnvelope /></div>
                <div>
                  <div className="info-label">Email</div>
                  <div className="info-val">Aurastonewholesale@gmail.com</div>
                </div>
              </div>

              <div className="info-item">
                <div className="info-icon-box"><FaMapMarkerAlt /></div>
                <div>
                  <div className="info-label">Address</div>
                  <div className="info-val">Khambhat, Gujarat, India</div>
                </div>
              </div>

              {/* <div className="info-item">
                <div className="info-icon-box"><FaBuilding /></div>
                <div>
                  <div className="info-label">GST Number</div>
                  <div className="info-val">24AAACU1234A1Z5</div>
                </div>
              </div> */}
            </div>

            <div className="whatsapp-chat-block">
              <a
                href="https://wa.me/919104139899"
                target="_blank"
                rel="noopener noreferrer"
                className="whatsapp-direct-btn"
              >
                <FaWhatsapp size={16} /> Direct WhatsApp Chat
              </a>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
