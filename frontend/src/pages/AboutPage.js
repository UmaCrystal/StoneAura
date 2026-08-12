import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FaGem, FaAward, FaCrown, FaHeadset, FaGlobeAsia, FaHistory, FaBriefcase } from 'react-icons/fa';
import './AboutPage.css';

export default function AboutPage() {
  const navigate = useNavigate();

  return (
    <div className="about-page">
      {/* HERO SECTION */}
      <section className="about-hero">
        <div className="about-hero-content">
          <div className="about-badge">✦ Handcrafted by Nature ✦</div>
          <h1>About <em>Aurastone</em></h1>
          <p>More than just beautiful stones – we bring you the pure energy of the Earth, ethically sourced and hand-curated.</p>
        </div>
      </section>

      {/* OUR STORY SECTION */}
      <section className="about-story-section">
        <div className="about-story-grid">
          <div className="about-story-visual">
            <div className="visual-card">
              <span className="visual-icon"><FaGem /></span>
              <h3>Aurastone</h3>
              <p className="visual-tag">More Than Beautiful</p>
              <div className="visual-gold-strip"></div>
            </div>
          </div>

          <div className="about-story-content">
            <div className="section-title-left">
              <h2>Our <span>Story</span></h2>
              <div className="title-divider"></div>
            </div>
            <p>
              Aurastone is a fresh, passionate startup born out of a deep love for natural gemstones and the healing power of crystals. We represent a new generation of crystal enthusiasts dedicated to bringing authenticity, clarity, and beauty to the modern world.
            </p>
            <p>
              Our journey began in Khambhat, the heart of gemstone craftsmanship. With a simple mission to make high-quality, authentic crystals accessible to everyone, we are driven by energy, transparency, and an absolute commitment to quality in every piece we source.
            </p>
            <p>
              Every bracelet and item in our collection is carefully selected, hand-polished to highlight its natural beauty, and checked for energetic purity. Whether you are looking for spiritual guidance, decor for your home, or a meaningful gift, we are here to connect you with the power of nature.
            </p>

            <div className="story-stats-grid">
              <div className="story-stat-card">
                <span className="stat-icon"><FaHistory /></span>
                <div className="stat-label">Founded</div>
                <div className="stat-value">2021</div>
              </div>
              <div className="story-stat-card">
                <span className="stat-icon"><FaGlobeAsia /></span>
                <div className="stat-label">Location</div>
                <div className="stat-value">Khambhat, India</div>
              </div>
              <div className="story-stat-card">
                <span className="stat-icon"><FaBriefcase /></span>
                <div className="stat-label">Nature of Business</div>
                <div className="stat-value">Retail & Wholesale</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CORE VALUES SECTION */}
      <section className="about-values-section">
        <div className="section-header">
          <h2>Our Core <span>Values</span></h2>
          <div className="divider"></div>
          <p>The principles that guide our work and quality standards at Aurastone.</p>
        </div>

        <div className="values-grid">
          {[
            {
              icon: <FaGem />,
              title: "100% Natural",
              desc: "Every single crystal we offer is verified natural and authentic, directly sourced from trusted miners."
            },
            {
              icon: <FaAward />,
              title: "Authentic & Trusted",
              desc: "We stand behind the source and spiritual energy of our crystals, providing transparency in every order."
            },
            {
              icon: <FaCrown />,
              title: "Premium Quality",
              desc: "Our local artisans handcraft and polish each gemstone piece to perfection, ensuring unmatched aesthetics."
            },
            {
              icon: <FaHeadset />,
              title: "Customer Support",
              desc: "Your journey with crystals matters. We provide personalized support and guidance for every customer."
            }
          ].map((val, idx) => (
            <div key={idx} className="value-card">
              <div className="value-icon-box">{val.icon}</div>
              <h3>{val.title}</h3>
              <p>{val.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CALL TO ACTION */}
      <section className="about-cta-section">
        <div className="about-cta-card">
          <h2>Ready to Explore Our Collection?</h2>
          <p>Find the perfect crystal bracelet that resonates with your energy and style.</p>
          <button className="cta-btn" onClick={() => navigate('/')}>
            Explore Products
          </button>
        </div>
      </section>
    </div>
  );
}
