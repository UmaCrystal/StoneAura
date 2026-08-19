
import React, { useState, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { useNavigate, useLocation,Link } from 'react-router-dom';
import { 
  FaGem, FaCog, FaSignOutAlt, FaSignInAlt,
  FaCircleNotch, FaBoxes, FaTree, FaFeatherAlt, 
  FaSun, FaPray, FaStar, FaRing, FaCrown, FaOm, FaMountain, 
  FaCircle, FaSeedling, FaCoins, FaEllipsisH, FaCertificate, 
  FaHandPaper, FaHeart, FaSpa, FaSyncAlt, FaMagic
} from 'react-icons/fa';
import { useAuth } from '../context/AuthContext';
import { useProducts } from '../context/ProductContext';
import AccountButton from './AccountButton';
import './Header.css';



const CATEGORY_ICONS = {
  "Gemstone Bracelets": <FaCircleNotch />,
  "Tumbled Stones": <FaBoxes />,
  "Pyramid Stone": <FaGem />,
  "Gemstone Tree": <FaTree />,
  "Selenite Stone": <FaFeatherAlt />,
  "Orgone Pyramid": <FaGem />,
  "Healing Crystals": <FaMagic />,
  "Chips": <FaMagic />,
  "CHIPS": <FaMagic />,
  "Rudraksha": <FaSun />,
  "Gemstone Angels": <FaPray />,
  "Unique Products": <FaStar />,
  "Hangings": <FaStar />,
  "HANGINGS": <FaStar />,
  "Jap Mala": <FaRing />,
  "Fancy Product": <FaCrown />,
  "Crystal Shivling": <FaOm />,
  "Rough Stone": <FaMountain />,
  "Gemstone Ball": <FaCircle />,
  "Crystal Flowers": <FaSeedling />,
  "Zibu Coins": <FaCoins />,
  "Tortoise": <FaSeedling />,
  "TORTOISE": <FaSeedling />,
  "Beads String 8mm": <FaEllipsisH />,
  "Gemstone Pendant": <FaCertificate />,
  "Pendants": <FaCertificate />,
  "Palm Stone": <FaHandPaper />,
  "Gemstone": <FaGem />,
  "Crystal Heart Stone": <FaHeart />,
  "Crystal Rakhi": <FaStar />,
  "Roller And Guasha": <FaSpa />,
  "Tumbled Bracelets": <FaSyncAlt />,
  "Anklets": <FaSpa />,
  "Bracelet Chip": <FaSyncAlt />,
  "Ring": <FaRing />,
  "ANKLET": <FaSpa />,
  "BRACELET CHIP": <FaSyncAlt />,
  "RING": <FaRing />
};

const getCategoryIcon = (cat) => CATEGORY_ICONS[cat] || <FaGem />;

export default function Header() {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [activeNav, setActiveNav] = useState('home');
  const { user, login, logout } = useAuth();
  const { taxonomy: TAXONOMY } = useProducts();
  const navigate = useNavigate();
  const location = useLocation();

  // Collapsible accordion for mobile
  const [mobileCollectionsOpen, setMobileCollectionsOpen] = useState(false);
  const [activeMobileColl, setActiveMobileColl] = useState(null);

  // Mobile login form states
  const [mobileLoginOpen, setMobileLoginOpen] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleCategoryClick = (e, col, cat) => {
    e.preventDefault();
    navigate(`/?collection=${encodeURIComponent(col)}&category=${encodeURIComponent(cat)}`);
    setTimeout(() => {
      const el = document.getElementById('products');
      if (el) el.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  };

  useEffect(() => {
    const handleScrollAndRoute = () => {
      setScrolled(window.scrollY > 20);
      const path = location.pathname;

      if (path === '/about') {
        setActiveNav('about');
        return;
      }
      if (path === '/contact') {
        setActiveNav('contact');
        return;
      }
      if (path === '/products') {
        setActiveNav('products');
        return;
      }

      // On home path "/"
      const scrollPos = window.scrollY;
      const contactEl = document.getElementById('contact');
      const aboutEl = document.getElementById('about');
      const productsEl = document.getElementById('products');

      if (contactEl && scrollPos >= contactEl.offsetTop - 180) {
        setActiveNav('contact');
      } else if (aboutEl && scrollPos >= aboutEl.offsetTop - 180) {
        setActiveNav('about');
      } else if (productsEl && scrollPos >= productsEl.offsetTop - 180) {
        setActiveNav('products');
      } else {
        setActiveNav('home');
      }
    };

    handleScrollAndRoute();
    window.addEventListener('scroll', handleScrollAndRoute);
    return () => window.removeEventListener('scroll', handleScrollAndRoute);
  }, [location.pathname]);

  // Lock body scroll when mobile menu is open
  useEffect(() => {
    if (menuOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [menuOpen]);

  // Reset mobile login when menu closes
  useEffect(() => {
    if (!menuOpen) {
      setMobileLoginOpen(false);
      setUsername("");
      setPassword("");
      setError("");
    }
  }, [menuOpen]);

  const handleMobileLogin = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(username, password);
      setMobileLoginOpen(false);
      setUsername("");
      setPassword("");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <header className={`header${scrolled ? ' scrolled' : ''}`}>
      <div className="header-inner">
        {/* <a href="/" className="logo">
          <img src="/images/logo-removebg-preview.png" alt="Aurastone" className="logo-img" />
          <div>
            <div className="logo-text">Aura<span>Stone</span></div>
            <div className="logo-tagline">More Than Beautiful</div>
          </div>
        </a> */}
        <Link to="/" className="logo">
          <img src="/images/logo1.png" alt="Aurastone" className="logo-img" />
        </Link>
        <nav className="nav">
          <Link to="/" className={activeNav === 'home' ? 'active' : ''}>Home</Link>
          <div className="nav-dropdown-trigger">
            <Link href="/#products" className={`nav-dropdown-title ${activeNav === 'products' ? 'active' : ''}`}>
              Products
            </Link>
            <div className="mega-menu">
              <div className="mega-menu-grid">
                {Object.keys(TAXONOMY).map(col => (
                  <div key={col} className="mega-menu-column">
                    <div className="mega-menu-header">{col}</div>
                    <ul className="mega-menu-links">
                      {TAXONOMY[col].map(cat => (
                        <li key={cat}>
                          <Link href={`/#products?collection=${encodeURIComponent(col)}&category=${encodeURIComponent(cat)}`} onClick={(e) => handleCategoryClick(e, col, cat)}>
                            <span className="cat-icon-inline">{getCategoryIcon(cat)}</span> {cat}
                          </Link>
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            </div>
          </div>
          <Link href="/about" className={activeNav === 'about' ? 'active' : ''}>About</Link>
          <Link href="/contact" className={activeNav === 'contact' ? 'active' : ''}>Contact</Link>
        </nav>

        <a
          href="https://wa.me/+919104139899"
          target="_blank"
          rel="noopener noreferrer"
          className="header-cta"
        >
          <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z" />
            <path d="M12 0C5.373 0 0 5.373 0 12c0 2.123.554 4.118 1.528 5.855L0 24l6.335-1.508A11.945 11.945 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.818a9.818 9.818 0 01-5.006-1.371l-.36-.214-3.727.977.994-3.634-.235-.374A9.818 9.818 0 1112 21.818z" />
          </svg>
          WhatsApp Us
        </a>

        <div className="header-account-desktop">
          <AccountButton />
        </div>

        <button
          className={`hamburger${menuOpen ? ' active' : ''}`}
          onClick={() => setMenuOpen(!menuOpen)}
          aria-label="Toggle menu"
          aria-expanded={menuOpen}
        >
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>

      {createPortal(
        <div className={`mobile-nav-overlay${menuOpen ? ' open' : ''}`} onClick={() => setMenuOpen(false)}>
          <div className="mobile-nav-drawer" onClick={(e) => e.stopPropagation()}>
            <button className="mobile-nav-close" onClick={() => setMenuOpen(false)} aria-label="Close menu">✕</button>
            <div className="mobile-nav-links">
              <Link href="/" onClick={() => setMenuOpen(false)}>Home</Link>

              <div className="mobile-accordion">
                <button
                  type="button"
                  className={`mobile-accordion-btn${mobileCollectionsOpen ? ' open' : ''}`}
                  onClick={() => setMobileCollectionsOpen(!mobileCollectionsOpen)}
                >
                  Collections <span>{mobileCollectionsOpen ? '▼' : '▶'}</span>
                </button>
                {mobileCollectionsOpen && (
                  <div className="mobile-accordion-content">
                    {Object.keys(TAXONOMY).map(col => (
                      <div key={col} className="mobile-sub-accordion">
                        <button
                          type="button"
                          className={`mobile-sub-accordion-btn${activeMobileColl === col ? ' active' : ''}`}
                          onClick={() => setActiveMobileColl(activeMobileColl === col ? null : col)}
                        >
                          {col} <span>{activeMobileColl === col ? '−' : '+'}</span>
                        </button>
                        {activeMobileColl === col && (
                          <div className="mobile-sub-links">
                            {TAXONOMY[col].map(cat => (
                              <Link
                                key={cat}
                                href={`/#products?collection=${encodeURIComponent(col)}&category=${encodeURIComponent(cat)}`}
                                onClick={(e) => {
                                  handleCategoryClick(e, col, cat);
                                  setMenuOpen(false);
                                }}
                              >
                                <span className="cat-icon-inline">{getCategoryIcon(cat)}</span> {cat}
                              </Link>
                            ))}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <Link href="/about" onClick={() => setMenuOpen(false)}>About</Link>
              <Link href="/contact" onClick={() => setMenuOpen(false)}>Contact</Link>

              <a
                href="https://wa.me/+919104139899"
                target="_blank"
                rel="noopener noreferrer"
                className="mobile-cta"
                onClick={() => setMenuOpen(false)}
              >
                WhatsApp Us
              </a>

              <div className="mobile-divider"></div>

              {/* Integrated Mobile User Actions */}
              {user ? (
                <div className="mobile-user-section">
                  <div className="mobile-user-info">
                    <div className="mobile-avatar">{user.username[0].toUpperCase()}</div>
                    <div>
                      <div className="mobile-username">{user.username}</div>
                      <div className="mobile-userole">{user.is_admin ? "Administrator" : "User"}</div>
                    </div>
                  </div>
                  {user.is_admin && (
                    <button className="mobile-nav-btn admin-btn" onClick={() => { navigate("/admin-dashboard"); setMenuOpen(false); }}>
                      <FaCog /> Admin Dashboard
                    </button>
                  )}
                  <button className="mobile-nav-btn logout-btn" onClick={() => { logout(); setMenuOpen(false); }}>
                    <FaSignOutAlt /> Log Out
                  </button>
                </div>
              ) : !mobileLoginOpen ? (
                <button className="mobile-nav-btn login-btn" onClick={() => { setMobileLoginOpen(true); setError(""); }}>
                  <FaSignInAlt /> Log In
                </button>
              ) : (
                <form onSubmit={handleMobileLogin} className="mobile-login-form">
                  <div className="mobile-login-header">
                    <h3>Sign In</h3>
                    <button type="button" className="mobile-login-back" onClick={() => setMobileLoginOpen(false)}>
                      ← Back
                    </button>
                  </div>
                  <div className="mobile-field">
                    <label>Username</label>
                    <input
                      type="text"
                      value={username}
                      onChange={e => setUsername(e.target.value)}
                      placeholder="Enter username"
                      required
                    />
                  </div>
                  <div className="mobile-field">
                    <label>Password</label>
                    <input
                      type="password"
                      value={password}
                      onChange={e => setPassword(e.target.value)}
                      placeholder="Enter password"
                      required
                    />
                  </div>
                  {error && <div className="mobile-login-error">{error}</div>}
                  <button type="submit" className="mobile-login-submit" disabled={loading}>
                    {loading ? "Signing in..." : "Sign In"}
                  </button>
                </form>
              )}
            </div>
          </div>
        </div>,
        document.body
      )}
    </header>
  );
}
