
import React from 'react';
import { Link } from 'react-router-dom';
import { FaMapMarkerAlt, FaPhone, FaEnvelope, FaBuilding, FaWhatsapp, FaInstagram } from 'react-icons/fa';
import './Footer.css';

export default function Footer() {
  return (
    <footer id="contact">
      <div className="footer-inner">
        <div className="footer-grid">
          <div className="footer-brand">
            <div className="logo-text">Uma <span>Crystal</span></div>
            <div className="logo-tagline">More Than Beautiful</div>
            <p>A fresh startup dedicated to premium gemstones and healing crystals. Crafted by nature, curated with passion.</p>
            <div className="footer-social">
              <a href="https://wa.me/9104139899" target="_blank" rel="noopener noreferrer" className="social-btn" aria-label="WhatsApp">
                <FaWhatsapp size={18} />
              </a>
              <a href="https://www.instagram.com/_umacrystal_" target="_blank" rel="noopener noreferrer" className="social-btn" aria-label="Instagram">
                <FaInstagram size={18} />
              </a>
            </div>
          </div>

          <div className="footer-col" id="about">
            <h4>Quick Links</h4>
            <ul>
              <li><a href="/">Home</a></li>
              <li><a href="/products">Bracelets</a></li>
              <li><a href="#about">About Us</a></li>
              <li><a href="#contact">Contact</a></li>
            </ul>
          </div>

          <div className="footer-col">
            <h4>Collections</h4>
            <ul>
              <li><Link to="/">Gemstone Bracelets</Link></li>
              <li><Link to="/?filter=Turquoise">Turquoise</Link></li>
              <li><Link to="/?filter=Seven%20Chakra">Seven Chakra</Link></li>
              <li><Link to="/?filter=Amethyst">Amethyst</Link></li>
            </ul>
          </div>

          <div className="footer-col">
            <h4>Contact Us</h4>
            <div className="footer-contact">
              <div className="contact-item"><span><FaMapMarkerAlt /></span><span>Khambhat, Gujarat, India</span></div>
              <div className="contact-item"><span><FaPhone /></span><span>+91 9104139899</span></div>
              <div className="contact-item"><span><FaEnvelope /></span><span>umacrystal2909@gmail.com</span></div>
              <div className="contact-item"><span><FaBuilding /></span><span>GSTIN: 24AAACU1234A1Z5</span></div>
            </div>
          </div>
        </div>

        <div className="footer-bottom">
          <span>© 2026 Uma Crystal. All Rights Reserved.</span>
          <span>Designed with elegance ✦</span>
        </div>
      </div>
    </footer>
  );
}
