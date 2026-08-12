
import React from 'react';
import { Link } from 'react-router-dom';
import {
  FaMapMarkerAlt, FaPhone, FaEnvelope, FaWhatsapp, FaInstagram,
  FaGem, FaCircleNotch, FaBoxes, FaTree, FaFeatherAlt, FaMagic,
  FaSun, FaPray, FaStar, FaRing, FaCrown, FaOm, FaMountain,
  FaCircle, FaSeedling, FaCoins, FaEllipsisH, FaCertificate,
  FaHandPaper, FaHeart, FaSpa, FaSyncAlt, FaLocationArrow
} from 'react-icons/fa';
import './Footer.css';

const TAXONOMY = {
  "BEST SELLERS": [
    "Gemstone Bracelets",
    "Tumbled Stones",
    "Pyramid Stone",
    "Gemstone Tree",
    "Selenite Stone",
    "Orgone Pyramid",
    "Healing Crystals"
  ],
  "SPIRITUAL & HEALING": [
    "Rudraksha",
    "Gemstone Angels",
    "Unique Products",
    "Jap Mala",
    "Fancy Product",
    "Crystal Shivling"
  ],
  "HOME & DECOR": [
    "Rough Stone",
    "Gemstone Ball",
    "Crystal Flowers",
    "Zibu Coin"
  ],
  "JEWELRY & ACCESSORIES": [
    "Beads String 8mm",
    "Gemstone Pendant",
    "Palm Stone",
    "Gemstone",
    "Crystal Heart Stone",
    "Crystal Rakhi",
    "Roller And Guasha",
    "Tumbled Bracelets"
  ]
};

const CATEGORY_ICONS = {
  "Gemstone Bracelets": <FaCircleNotch />,
  "Tumbled Stones": <FaBoxes />,
  "Pyramid Stone": <FaGem />,
  "Gemstone Tree": <FaTree />,
  "Selenite Stone": <FaFeatherAlt />,
  "Orgone Pyramid": <FaLocationArrow />,
  "Healing Crystals": <FaMagic />,
  "Rudraksha": <FaSun />,
  "Gemstone Angels": <FaPray />,
  "Unique Products": <FaStar />,
  "Jap Mala": <FaRing />,
  "Fancy Product": <FaCrown />,
  "Crystal Shivling": <FaOm />,
  "Rough Stone": <FaMountain />,
  "Gemstone Ball": <FaCircle />,
  "Crystal Flowers": <FaSeedling />,
  "Zibu Coin": <FaCoins />,
  "Beads String 8mm": <FaEllipsisH />,
  "Gemstone Pendant": <FaCertificate />,
  "Palm Stone": <FaHandPaper />,
  "Gemstone": <FaGem />,
  "Crystal Heart Stone": <FaHeart />,
  "Crystal Rakhi": <FaStar />,
  "Roller And Guasha": <FaSpa />,
  "Tumbled Bracelets": <FaSyncAlt />
};

const getCategoryIcon = (cat) => CATEGORY_ICONS[cat] || <FaGem />;

export default function Footer() {
  const handleScrollToProducts = () => {
    setTimeout(() => {
      const el = document.getElementById('products');
      if (el) el.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  };

  // Flatten TAXONOMY categories for the footer columns
  const allCategories = [];
  Object.keys(TAXONOMY).forEach(col => {
    TAXONOMY[col].forEach(cat => {
      allCategories.push({ collection: col, category: cat });
    });
  });

  // Split categories into two lists for columns
  const midIndex = Math.ceil(allCategories.length / 2);
  const col1 = allCategories.slice(0, midIndex);
  const col2 = allCategories.slice(midIndex);

  return (
    <footer id="contact">
      <div className="footer-inner">
        <div className="footer-grid">
          {/* Brand Column */}
          <div className="footer-brand">
            <div className="logo-brand-wrap" style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
              <img src="/images/logo.jpeg" alt="Aurastone" className="logo-img" style={{ width: '40px', height: '40px', borderRadius: '50%', objectFit: 'cover', border: '1px solid rgba(201,168,76,0.3)' }} />
              <div>
                <div className="logo-text" style={{ fontSize: '1.4rem', fontFamily: "'Cormorant Garamond', serif", fontWeight: '600', color: '#fff' }}>Aura<span>stone</span></div>
                <div className="logo-tagline" style={{ fontSize: '0.6rem', marginTop: '-2px', textTransform: 'uppercase', color: 'var(--gold-light)', letterSpacing: '0.15em' }}>"MORE THAN BEAUTIFUL"</div>
              </div>
            </div>
            <p className="brand-desc">
              A fresh startup dedicated to premium gemstones and healing crystals. Crafted by nature, curated with passion. We represent a new generation of quality and transparency in the world of crystals.
            </p>
            <div className="footer-social">
              <a href="https://wa.me/9104139899" target="_blank" rel="noopener noreferrer" className="social-btn" aria-label="WhatsApp">
                <FaWhatsapp size={16} />
              </a>
              <a href="https://www.instagram.com/aurastone.wholesale" target="_blank" rel="noopener noreferrer" className="social-btn" aria-label="Instagram">
                <FaInstagram size={16} />
              </a>
              {/* <a href="https://facebook.com" target="_blank" rel="noopener noreferrer" className="social-btn" aria-label="Facebook">
                <FaFacebookF size={16} />
              </a> */}
            </div>
          </div>

          {/* Quick Links & Contact Column */}
          <div className="footer-col">
            <h4>Quick Links</h4>
            <ul className="quick-links-list">
              <li><a href="/">Home</a></li>
              <li><a href="/#products" onClick={handleScrollToProducts}>Products</a></li>
              <li><a href="/about">About Us</a></li>
              <li><a href="/contact">Contact Us</a></li>
            </ul>

            <div className="footer-contact-info">
              <div className="contact-item">
                <span className="contact-icon"><FaMapMarkerAlt /></span>
                <span>Khambhat, Gujarat</span>
              </div>
              <div className="contact-item">
                <span className="contact-icon"><FaPhone style={{ transform: 'rotate(90deg)' }} /></span>
                <span>+91 9104139899</span>
              </div>
              <div className="contact-item">
                <span className="contact-icon"><FaEnvelope /></span>
                <span>Aurastonewholesale@gmail.com</span>
              </div>
              {/* <div className="contact-item">
                <span className="contact-icon"><FaBuilding /></span>
                <span>GSTIN: 24AAACU1234A1Z5</span>
              </div> */}
            </div>
          </div>

          {/* Our Collections Column */}
          <div className="footer-col collections-col">
            <h4>Our Collections</h4>
            <div className="collections-double-grid">
              <ul className="footer-cat-list">
                {col1.map((item, idx) => (
                  <li key={idx} className="footer-cat-item">
                    <span className="cat-icon-inline">{getCategoryIcon(item.category)}</span>
                    <Link
                      to={`/?collection=${encodeURIComponent(item.collection)}&category=${encodeURIComponent(item.category)}`}
                      onClick={handleScrollToProducts}
                    >
                      {item.category}
                    </Link>
                  </li>
                ))}
              </ul>
              <ul className="footer-cat-list">
                {col2.map((item, idx) => (
                  <li key={idx} className="footer-cat-item">
                    <span className="cat-icon-inline">{getCategoryIcon(item.category)}</span>
                    <Link
                      to={`/?collection=${encodeURIComponent(item.collection)}&category=${encodeURIComponent(item.category)}`}
                      onClick={handleScrollToProducts}
                    >
                      {item.category}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        {/* Footer Bottom */}
        <div className="footer-bottom">
          <span>© 2026 aurastone.wholsale. All Rights Reserved.</span>
        </div>
      </div>
    </footer>
  );
}
