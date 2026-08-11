
import React, { useState, useEffect } from 'react';
import AccountButton from './AccountButton';
import './Header.css';

export default function Header() {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', onScroll);
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  return (
    <header className={`header${scrolled ? ' scrolled' : ''}`}>
      <div className="header-inner">
        <a href="/" className="logo">
          <div className="logo-icon">💎</div>
          <div>
            <div className="logo-text">Uma <span>Crystal</span></div>
            <div className="logo-tagline">More Than Beautiful</div>
          </div>
        </a>

        <nav className="nav">
          <a href="/">Home</a>
          <a href="#products">Bracelets</a>
          <a href="#contact">Contact</a>
        </nav>

        <a
          href="https://wa.me/919510010383"
          target="_blank"
          rel="noopener noreferrer"
          className="header-cta"
        >
          <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/>
            <path d="M12 0C5.373 0 0 5.373 0 12c0 2.123.554 4.118 1.528 5.855L0 24l6.335-1.508A11.945 11.945 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.818a9.818 9.818 0 01-5.006-1.371l-.36-.214-3.727.977.994-3.634-.235-.374A9.818 9.818 0 1112 21.818z"/>
          </svg>
          WhatsApp Us
        </a>

        <AccountButton />

        <button
          className="hamburger"
          onClick={() => setMenuOpen(!menuOpen)}
          aria-label="Toggle menu"
        >
          <span className={menuOpen ? 'open' : ''}></span>
          <span className={menuOpen ? 'open' : ''}></span>
          <span className={menuOpen ? 'open' : ''}></span>
        </button>
      </div>

      {menuOpen && (
        <div className="mobile-nav">
          <a href="/" onClick={() => setMenuOpen(false)}>Home</a>
          <a href="#products" onClick={() => setMenuOpen(false)}>Bracelets</a>
          <a href="#contact" onClick={() => setMenuOpen(false)}>Contact</a>
          <a
            href="https://wa.me/919510010383"
            target="_blank"
            rel="noopener noreferrer"
            className="mobile-cta"
          >WhatsApp Us</a>
          <button className="mobile-close" onClick={() => setMenuOpen(false)}>✕</button>
        </div>
      )}
    </header>
  );
}
