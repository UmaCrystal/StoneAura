import React from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  FaGem, FaCircleNotch, FaBoxes, FaTree, FaFeatherAlt, FaMagic, 
  FaSun, FaPray, FaStar, FaRing, FaCrown, FaOm, FaMountain, 
  FaCircle, FaSeedling, FaCoins, FaEllipsisH, FaCertificate, 
  FaHandPaper, FaHeart, FaSpa, FaSyncAlt, FaLocationArrow 
} from 'react-icons/fa';
import './CategoriesPage.css';

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
    "Tumbled Bracelets",
    "Anklets"
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

export default function CategoriesPage() {
  const navigate = useNavigate();

  const handleCategorySelect = (col, cat) => {
    navigate(`/?collection=${encodeURIComponent(col)}&category=${encodeURIComponent(cat)}#products`);
    setTimeout(() => {
      const el = document.getElementById('products');
      if (el) el.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  };

  return (
    <div className="categories-page">
      {/* HERO SECTION */}
      <section className="categories-hero">
        <div className="categories-hero-content">
          <div className="categories-badge">✦ Natural Energy Catalog ✦</div>
          <h1>Explore <em>Our Collections</em></h1>
          <p>Browse through our hand-curated collections and choose the perfect energetic category for your journey.</p>
        </div>
      </section>

      {/* CATEGORIES DISPLAY SECTION */}
      <section className="categories-list-section">
        {Object.keys(TAXONOMY).map(col => (
          <div key={col} className="collection-group">
            <div className="collection-group-header">
              <h2>{col}</h2>
              <div className="header-line"></div>
            </div>

            <div className="categories-card-grid">
              {TAXONOMY[col].map(cat => (
                <div 
                  key={cat} 
                  className="category-showcase-card"
                  onClick={() => handleCategorySelect(col, cat)}
                >
                  <div className="card-hover-border"></div>
                  <div className="category-card-inner">
                    <div className="category-card-icon">
                      {getCategoryIcon(cat)}
                    </div>
                    <h3>{cat}</h3>
                    <p className="category-card-desc">
                      Premium authentic {cat.toLowerCase()} hand-finished for high spiritual frequency and visual perfection.
                    </p>
                    <div className="category-card-action">
                      Explore Products <span>→</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </section>
    </div>
  );
}
