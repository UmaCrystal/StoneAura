import React from "react";
import { Link, useLocation } from "react-router-dom";
import {
  FaMapMarkerAlt,
  FaPhone,
  FaEnvelope,
  FaWhatsapp,
  FaInstagram,
  FaGem,
  FaCircleNotch,
  FaBoxes,
  FaTree,
  FaFeatherAlt,
  FaMagic,
  FaSun,
  FaPray,
  FaStar,
  FaRing,
  FaCrown,
  FaOm,
  FaMountain,
  FaCircle,
  FaSeedling,
  FaCoins,
  FaEllipsisH,
  FaCertificate,
  FaHandPaper,
  FaHeart,
  FaSpa,
  FaSyncAlt,
} from "react-icons/fa";
import { useProducts } from "../context/ProductContext";
import "./Footer.css";

const CATEGORY_ICONS = {
  "Gemstone Bracelets": <FaCircleNotch />,
  "Tumbled Stones": <FaBoxes />,
  "Pyramid Stone": <FaGem />,
  "Gemstone Tree": <FaTree />,
  "Selenite Stone": <FaFeatherAlt />,
  "Orgone Pyramid": <FaGem />,
  "Healing Crystals": <FaMagic />,
  Chips: <FaMagic />,
  CHIPS: <FaMagic />,
  Rudraksha: <FaSun />,
  "Gemstone Angels": <FaPray />,
  "Unique Products": <FaStar />,
  Hangings: <FaStar />,
  HANGINGS: <FaStar />,
  "Jap Mala": <FaRing />,
  "Fancy Product": <FaCrown />,
  "Crystal Shivling": <FaOm />,
  "Rough Stone": <FaMountain />,
  "Gemstone Ball": <FaCircle />,
  "Crystal Flowers": <FaSeedling />,
  "Zibu Coins": <FaCoins />,
  Tortoise: <FaSeedling />,
  TORTOISE: <FaSeedling />,
  "Beads String 8mm": <FaEllipsisH />,
  "Gemstone Pendant": <FaCertificate />,
  Pendants: <FaCertificate />,
  "Palm Stone": <FaHandPaper />,
  Gemstone: <FaGem />,
  "Crystal Heart Stone": <FaHeart />,
  "Crystal Rakhi": <FaStar />,
  "Roller And Guasha": <FaSpa />,
  "Tumbled Bracelets": <FaSyncAlt />,
  Anklets: <FaSpa />,
  "Bracelet Chip": <FaSyncAlt />,
  Ring: <FaRing />,
  ANKLET: <FaSpa />,
  "BRACELET CHIP": <FaSyncAlt />,
  RING: <FaRing />,
};

const getCategoryIcon = (cat) => CATEGORY_ICONS[cat] || <FaGem />;

export default function Footer() {
  const { taxonomy: TAXONOMY } = useProducts();
  const location = useLocation();
  const handleScrollToProducts = () => {
    setTimeout(() => {
      const el = document.getElementById("products");
      if (el) {
        const y = el.getBoundingClientRect().top + window.scrollY - 100;
        window.scrollTo({ top: y, behavior: "smooth" });
      } else if (location.pathname !== "/") {
        window.scrollTo({ top: 0, behavior: "smooth" });
      }
    }, 150);
  };

  const allCategories = [];
  Object.keys(TAXONOMY).forEach((col) => {
    TAXONOMY[col].forEach((cat) => {
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
            <Link
              to="/"
              className="logo-brand-wrap"
              onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
            >
              <img
                src="/images/logo1.png"
                alt="Aurastone"
                className="footer-logo-img"
              />
            </Link>
            <p className="brand-desc">
              With 15+ years of experience in the crystal & spiritual products
              industry, we offer premium-quality products at competitive
              wholesale prices.
            </p>
            <p className="brand-desc">💎 Quality Products</p>
            <p className="brand-desc">📦 Bulk Orders</p>
            <p className="brand-desc">🤝 Trusted Wholesale Partner</p>
            <div className="footer-social">
              <a
                href="https://wa.me/9104139899"
                target="_blank"
                rel="noopener noreferrer"
                className="social-btn"
                aria-label="WhatsApp"
              >
                <FaWhatsapp size={16} />
              </a>
              <a
                href="https://www.instagram.com/aurastone.wholesale"
                target="_blank"
                rel="noopener noreferrer"
                className="social-btn"
                aria-label="Instagram"
              >
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
              <li>
                <Link
                  to="/"
                  onClick={() =>
                    window.scrollTo({ top: 0, behavior: "smooth" })
                  }
                >
                  Home
                </Link>
              </li>
              <li>
                <Link to="/#products" onClick={handleScrollToProducts}>
                  Products
                </Link>
              </li>
              <li>
                <Link to="/about">About Us</Link>
              </li>
              <li>
                <Link to="/contact">Contact Us</Link>
              </li>
            </ul>

            <div className="footer-contact-info">
              <div className="contact-item">
                <span className="contact-icon">
                  <FaMapMarkerAlt />
                </span>
                <span>Khambhat, Gujarat</span>
              </div>
              <div className="contact-item">
                <span className="contact-icon">
                  <FaPhone style={{ transform: "rotate(90deg)" }} />
                </span>
                <span>+91 9104139899</span>
              </div>
              <div className="contact-item">
                <span className="contact-icon">
                  <FaEnvelope />
                </span>
                <span>aurastonewholesale@gmail.com</span>
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
                    <span className="cat-icon-inline">
                      {getCategoryIcon(item.category)}
                    </span>
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
                    <span className="cat-icon-inline">
                      {getCategoryIcon(item.category)}
                    </span>
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
