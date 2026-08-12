import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useSearchParams } from 'react-router-dom';
import { FaGem, FaTruck, FaWhatsapp, FaExclamationTriangle } from 'react-icons/fa';
import { HiSparkles } from 'react-icons/hi';
import ProductCard from '../components/ProductCard';
import ProductModal from '../components/ProductModal';
import './ProductsPage.css';

// Relative URL fallback — works whether running on port 8000, 3000, or any host
const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const STONE_FILTERS = [
  'Amethyst', 'Amazonite', 'Black Obsidian', 'Calcite', 'Carnelian',
  'Citrine', 'Green Aventurine', 'Green Jade', 'Howlite',
  'Lapis Lazuli', 'Lava', 'Moonstone', 'Opalite',
  'Peacock Ore', 'Pyrite', 'Rhodochrosite', 'Rhodonite',
  'Rose Quartz', 'Seven Chakra', 'Sodalite', 'Sunstone',
  'Tiger Eye', 'Turquoise',
];

const SORT_OPTIONS = [
  { value: 'name',   label: 'Name: A–Z' },
  { value: '-name',  label: 'Name: Z–A' },
  { value: 'price',  label: 'Price: Low → High' },
  { value: '-price', label: 'Price: High → Low' },
];

export default function ProductsPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const activeFilter = searchParams.get('filter') || 'All';

  const [products, setProducts]         = useState([]);
  const [filtered, setFiltered]         = useState([]);
  const [loading, setLoading]           = useState(true);
  const [error, setError]               = useState(null);
  const [search, setSearch]             = useState('');
  const [sortBy, setSortBy]             = useState('name');
  const [modalProduct, setModalProduct] = useState(null);
  const [backTop, setBackTop]           = useState(false);
  const [filterOpen, setFilterOpen]     = useState(false);
  const [sortOpen, setSortOpen]         = useState(false);
  const filterRef = useRef(null);
  const sortRef   = useRef(null);
  const searchRef = useRef(null);

  /* ── Fetch products ─────────────────────────────────────────────────────── */
  const loadProducts = useCallback(() => {
    const controller = new AbortController();
    setLoading(true);
    setError(null);
    fetch(`${API_BASE}/products/?ordering=${sortBy}&page_size=100`, {
      signal: controller.signal,
      headers: { Accept: 'application/json' },
    })
      .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then(data => {
        const items = Array.isArray(data) ? data : (data.results || []);
        setProducts(items);
        setLoading(false);
      })
      .catch(err => {
        if (err.name !== 'AbortError') {
          setError(err.message);
          setLoading(false);
        }
      });
    return () => controller.abort();
  }, [sortBy]);

  useEffect(() => {
    const cleanup = loadProducts();
    return cleanup;
  }, [loadProducts]);

  /* ── Filter + search ────────────────────────────────────────────────────── */
  useEffect(() => {
    let result = [...products];
    if (activeFilter !== 'All') {
      result = result.filter(p =>
        p.stone_type?.toLowerCase().includes(activeFilter.toLowerCase()) ||
        p.name?.toLowerCase().includes(activeFilter.toLowerCase())
      );
    }
    if (search.trim()) {
      const q = search.toLowerCase();
      result = result.filter(p =>
        p.name?.toLowerCase().includes(q) ||
        p.stone_type?.toLowerCase().includes(q) ||
        p.color?.toLowerCase().includes(q) ||
        p.material?.toLowerCase().includes(q)
      );
    }
    setFiltered(result);
  }, [search, activeFilter, products]);

  // Scroll to products grid when activeFilter changes to a specific gemstone
  useEffect(() => {
    if (activeFilter !== 'All') {
      const el = document.getElementById('products');
      if (el) {
        el.scrollIntoView({ behavior: 'smooth' });
      }
    }
  }, [activeFilter]);

  /* ── Close dropdowns on outside click ──────────────────────────────────── */
  useEffect(() => {
    const handler = (e) => {
      if (filterRef.current && !filterRef.current.contains(e.target)) setFilterOpen(false);
      if (sortRef.current   && !sortRef.current.contains(e.target))   setSortOpen(false);
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  /* ── Back-to-top ────────────────────────────────────────────────────────── */
  useEffect(() => {
    const onScroll = () => setBackTop(window.scrollY > 400);
    window.addEventListener('scroll', onScroll);
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  /* ── Fade-in observer ───────────────────────────────────────────────────── */
  useEffect(() => {
    const observer = new IntersectionObserver(
      entries => entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); }),
      { threshold: 0.1 }
    );
    document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
    return () => observer.disconnect();
  }, [filtered]);

  /* ── Particles ──────────────────────────────────────────────────────────── */
  useEffect(() => {
    const container = document.getElementById('particles');
    if (!container || container.childElementCount > 0) return;
    for (let i = 0; i < 20; i++) {
      const p = document.createElement('div');
      p.className = 'particle';
      p.style.cssText = `left:${Math.random()*100}%;top:${Math.random()*100}%;animation-delay:${Math.random()*6}s;animation-duration:${4+Math.random()*4}s`;
      container.appendChild(p);
    }
  }, []);

  const openModal  = useCallback(p => setModalProduct(p), []);
  const closeModal = useCallback(() => setModalProduct(null), []);

  const activeSortLabel = SORT_OPTIONS.find(o => o.value === sortBy)?.label || 'Sort';

  const handleFilterSelect = (f) => {
    const newParams = new URLSearchParams(searchParams);
    if (f === 'All') {
      newParams.delete('filter');
    } else {
      newParams.set('filter', f);
    }
    setSearchParams(newParams);
    setFilterOpen(false);
  };

  const handleSortSelect = (v) => {
    setSortBy(v);
    setSortOpen(false);
  };

  return (
    <>
      {/* ── HERO ── */}
      <section className="hero" id="home">
        <div className="hero-particles" id="particles"></div>
        <div className="hero-content">
          <div className="hero-badge">✦ Authentic Natural Crystals ✦</div>
          <h1>Wear the <em>Energy</em><br />of the Earth</h1>
          <p>Premium gemstone bracelets handcrafted in Khambhat, Gujarat. Each piece carries the healing power of authentic natural crystals.</p>
          <button className="hero-btn" onClick={() => document.getElementById('products')?.scrollIntoView({ behavior: 'smooth' })}>
            Explore Collection
            <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M12 4l-1.41 1.41L16.17 11H4v2h12.17l-5.58 5.59L12 20l8-8z"/></svg>
          </button>
          <div className="hero-stats">
            <div className="stat"><span className="stat-num">40+</span><span className="stat-label">Bracelet Varieties</span></div>
            <div className="stat"><span className="stat-num">100%</span><span className="stat-label">Natural Gemstones</span></div>
            <div className="stat"><span className="stat-num">5000+</span><span className="stat-label">Happy Customers</span></div>
            <div className="stat"><span className="stat-num">₹87</span><span className="stat-label">Starting Price</span></div>
          </div>
        </div>
        <div className="hero-scroll"><div className="scroll-line"></div>Scroll</div>
      </section>

      {/* ── TRUST STRIP ── */}
      <div className="trust-strip">
        <div className="trust-inner">
          {[
            { icon: <FaGem />, title: '100% Natural',        sub: 'Authentic gemstones' },
            { icon: <FaTruck />, title: 'Pan India Delivery',  sub: 'Fast & secure shipping' },
            { icon: <FaWhatsapp />, title: 'WhatsApp Support',    sub: 'Instant response' },
            { icon: <HiSparkles />, title: 'Handcrafted',          sub: 'Made with love' },
          ].map(t => (
            <div key={t.title} className="trust-item">
              <div className="trust-icon">{t.icon}</div>
              <div className="trust-text"><strong>{t.title}</strong><span>{t.sub}</span></div>
            </div>
          ))}
        </div>
      </div>

      {/* ── TOOLBAR ── */}
      <div className="toolbar" id="products">
        <div className="toolbar-inner">

          {/* Search */}
          <div className="tb-search">
            <svg className="tb-search-icon" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
            <input
              ref={searchRef}
              type="search"
              placeholder="Search bracelets…"
              value={search}
              onChange={e => setSearch(e.target.value)}
              aria-label="Search bracelets"
              autoComplete="off"
            />
            {search && (
              <button className="tb-clear" onClick={() => setSearch('')} aria-label="Clear search">✕</button>
            )}
          </div>

          {/* Filter dropdown */}
          <div className="tb-dropdown-wrap" ref={filterRef}>
            <button
              className={`tb-btn${filterOpen ? ' open' : ''}${activeFilter !== 'All' ? ' active' : ''}`}
              onClick={() => { setFilterOpen(o => !o); setSortOpen(false); }}
              aria-haspopup="listbox"
              aria-expanded={filterOpen}
            >
              <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" strokeWidth="2.2"><path d="M22 3H2l8 9.46V19l4 2v-8.54L22 3z"/></svg>
              {activeFilter === 'All' ? 'Filter by Stone' : activeFilter}
              <svg className={`tb-chevron${filterOpen ? ' up' : ''}`} viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M6 9l6 6 6-6"/></svg>
            </button>

            {filterOpen && (
              <div className="tb-dropdown" role="listbox">
                <div className="tb-dropdown-header">Filter by Stone</div>
                <button
                  className={`tb-option${activeFilter === 'All' ? ' selected' : ''}`}
                  onClick={() => handleFilterSelect('All')}
                  role="option"
                  aria-selected={activeFilter === 'All'}
                >
                  <span className="tb-option-dot"></span>
                  All Bracelets
                  {activeFilter === 'All' && <svg className="tb-check" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M20 6L9 17l-5-5"/></svg>}
                </button>
                <div className="tb-dropdown-divider"/>
                {STONE_FILTERS.map(f => (
                  <button
                    key={f}
                    className={`tb-option${activeFilter === f ? ' selected' : ''}`}
                    onClick={() => handleFilterSelect(f)}
                    role="option"
                    aria-selected={activeFilter === f}
                  >
                    <span className="tb-option-dot"></span>
                    {f}
                    {activeFilter === f && <svg className="tb-check" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M20 6L9 17l-5-5"/></svg>}
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Sort dropdown */}
          <div className="tb-dropdown-wrap" ref={sortRef}>
            <button
              className={`tb-btn${sortOpen ? ' open' : ''}`}
              onClick={() => { setSortOpen(o => !o); setFilterOpen(false); }}
              aria-haspopup="listbox"
              aria-expanded={sortOpen}
            >
              <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" strokeWidth="2.2"><path d="M3 6h18M7 12h10M11 18h2"/></svg>
              {activeSortLabel}
              <svg className={`tb-chevron${sortOpen ? ' up' : ''}`} viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M6 9l6 6 6-6"/></svg>
            </button>

            {sortOpen && (
              <div className="tb-dropdown" role="listbox">
                <div className="tb-dropdown-header">Sort by</div>
                {SORT_OPTIONS.map(o => (
                  <button
                    key={o.value}
                    className={`tb-option${sortBy === o.value ? ' selected' : ''}`}
                    onClick={() => handleSortSelect(o.value)}
                    role="option"
                    aria-selected={sortBy === o.value}
                  >
                    <span className="tb-option-dot"></span>
                    {o.label}
                    {sortBy === o.value && <svg className="tb-check" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M20 6L9 17l-5-5"/></svg>}
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Active filter pill + clear */}
          {(activeFilter !== 'All' || search) && (
            <button
              className="tb-clear-all"
              onClick={() => {
                setSearch('');
                const newParams = new URLSearchParams(searchParams);
                newParams.delete('filter');
                setSearchParams(newParams);
              }}
            >
              Clear all ✕
            </button>
          )}

          {/* Count */}
          {!loading && !error && (
            <span className="tb-count">
              {filtered.length} {filtered.length === 1 ? 'bracelet' : 'bracelets'}
            </span>
          )}
        </div>
      </div>

      {/* ── PRODUCTS SECTION ── */}
      <section className="products-section">
        <div className="section-header fade-in">
          <h2>Gemstone <span>Bracelets</span></h2>
          <div className="divider"></div>
          <p>Explore our premium collection of authentic gemstone bracelets for spiritual healing, wellness, and aesthetic beauty.</p>
        </div>

        {/* Loading skeletons */}
        {loading && (
          <div className="products-grid">
            {Array.from({ length: 8 }).map((_, i) => (
              <div key={i} className="skeleton-card">
                <div className="skeleton skeleton-img"></div>
                <div className="skeleton-body">
                  <div className="skeleton skeleton-line short"></div>
                  <div className="skeleton skeleton-line"></div>
                  <div className="skeleton skeleton-line medium"></div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Error state — auto-retries, no manual button needed */}
        {error && !loading && (
          <div className="error-state">
            <div className="error-icon"><FaExclamationTriangle /></div>
            <p>Could not load products.</p>
            <button onClick={loadProducts} className="retry-btn">Try again</button>
          </div>
        )}

        {/* Empty filter result */}
        {!loading && !error && filtered.length === 0 && (
          <div className="empty-state">
            <div className="empty-icon"><FaGem /></div>
            <h3>No bracelets found</h3>
            <p>Try a different search or filter</p>
            <button onClick={() => {
              setSearch('');
              const newParams = new URLSearchParams(searchParams);
              newParams.delete('filter');
              setSearchParams(newParams);
            }} className="retry-btn">
              Clear Filters
            </button>
          </div>
        )}

        {/* Product grid */}
        {!loading && !error && filtered.length > 0 && (
          <div className="products-grid">
            {filtered.map(product => (
              <div key={product.id} className="fade-in">
                <ProductCard product={product} onOpenModal={openModal} />
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Modal */}
      {modalProduct && <ProductModal product={modalProduct} onClose={closeModal} />}

      {/* Back to top */}
      <button
        className={`back-top${backTop ? ' visible' : ''}`}
        onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
        aria-label="Back to top"
      >↑</button>
    </>
  );
}
