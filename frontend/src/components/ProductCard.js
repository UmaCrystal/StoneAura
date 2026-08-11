import React, { useState } from 'react';
import './ProductCard.css';

const BEAD_SIZES = ['6mm', '8mm', '12mm'];

const WA_ICON = (
  <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor" aria-hidden="true">
    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z" />
    <path d="M12 0C5.373 0 0 5.373 0 12c0 2.123.554 4.118 1.528 5.855L0 24l6.335-1.508A11.945 11.945 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.818a9.818 9.818 0 01-5.006-1.371l-.36-.214-3.727.977.994-3.634-.235-.374A9.818 9.818 0 1112 21.818z" />
  </svg>
);

// ── Sub-component: handles error states gracefully ──────────────────
function ProductImage({ src, alt, stoneName }) {
  const [hasError, setHasError] = useState(false);

  const isPlaceholder = src?.includes('placehold.co');

  if (isPlaceholder || hasError) {
    return (
      <div className="img-placeholder" aria-label={alt}>
        <div className="img-placeholder-inner">
          <span className="img-placeholder-gem">💎</span>
          <span className="img-placeholder-name">{stoneName || alt}</span>
        </div>
      </div>
    );
  }

  return (
    <img
      src={src}
      alt={alt}
      onError={() => setHasError(true)}
    />
  );
}

// ── Main component ─────────────────────────────────────────────────────────
export default function ProductCard({ product, onOpenModal }) {
  const [selectedSize, setSelectedSize] = useState('8mm');
  const [wishlisted, setWishlisted] = useState(false);

  const handleQuote = (e) => {
    e.stopPropagation();
    const text = encodeURIComponent(
      `Hi, I am interested in ${product.name} (Size: ${selectedSize}) — price: ₹${product.price}`
    );
    window.open(`https://wa.me/9104139899?text=${text}`, '_blank', 'noopener,noreferrer');
  };

  const handleWishlist = (e) => {
    e.stopPropagation();
    setWishlisted(w => !w);
  };

  const handleQuickView = (e) => {
    e.stopPropagation();
    onOpenModal(product);
  };

  const displayProps = [
    product.stone_type && { key: 'Stone', val: product.stone_type },
    product.bead_size && { key: 'Size', val: product.bead_size },
  ].filter(Boolean);

  return (
    <article
      className="product-card"
      onClick={() => onOpenModal(product)}
      tabIndex={0}
      role="button"
      onKeyDown={e => e.key === 'Enter' && onOpenModal(product)}
      aria-label={`View details for ${product.name}`}
    >
      {/* ── Badges ── */}
      {product.is_featured && (
        <div className="card-badge" aria-label="Featured product">✦ Featured</div>
      )}

      <button
        className={`card-wishlist${wishlisted ? ' active' : ''}`}
        onClick={handleWishlist}
        aria-label={wishlisted ? 'Remove from wishlist' : 'Add to wishlist'}
        aria-pressed={wishlisted}
      >
        {wishlisted ? '♥' : '♡'}
      </button>

      {/* ── Image ── */}
      <div className="card-image-wrap">
        <ProductImage
          src={product.image_url}
          alt={product.name}
          stoneName={product.stone_type}
        />
        <div className="img-overlay" aria-hidden="true" />
        <button className="quick-view" onClick={handleQuickView}>
          Quick View
        </button>
      </div>

      {/* ── Body ── */}
      <div className="card-body">
        <div className="card-meta">
          {product.stone_type && (
            <span className="stone-type">{product.stone_type}</span>
          )}
          <div className="card-rating" aria-label="4.8 out of 5 stars">
            <span className="stars" aria-hidden="true">★★★★★</span>
            <span>(4.8)</span>
          </div>
        </div>

        <h3 className="card-title">{product.name}</h3>

        {displayProps.length > 0 && (
          <div className="card-props">
            {displayProps.map(p => (
              <span key={p.key} className="prop-tag">
                {p.key}: {p.val}
              </span>
            ))}
          </div>
        )}

        {/* ── Bead size selector ── */}
        <div
          className="size-section"
          onClick={e => e.stopPropagation()}
          role="group"
          aria-label="Select bead size"
        >
          <div className="size-label">Bead Size</div>
          <div className="size-options">
            {BEAD_SIZES.map(sz => (
              <button
                key={sz}
                className={`size-btn${selectedSize === sz ? ' selected' : ''}`}
                onClick={() => setSelectedSize(sz)}
                aria-label={`Bead size ${sz}`}
                aria-pressed={selectedSize === sz}
              >
                {sz}
              </button>
            ))}
          </div>
        </div>

        {/* ── Footer: price + tiers + CTA ── */}
        <div className="card-footer">
          <div className="price-wrap">
            <span className="price">₹{product.price}</span>
            <span className="price-unit">per piece</span>
          </div>

          {(product.price_10pc || product.price_50pc) && (
            <div className="price-tiers" aria-label="Bulk pricing">
              {product.price_10pc && (
                <span className="tier-tag">10pc: ₹{product.price_10pc}</span>
              )}
              {product.price_50pc && (
                <span className="tier-tag">50pc: ₹{product.price_50pc}</span>
              )}
            </div>
          )}

          <button
            className="btn-quote"
            onClick={handleQuote}
            aria-label={`Get WhatsApp quote for ${product.name}`}
          >
            {WA_ICON}
            Get Quote
          </button>
        </div>
      </div>
    </article>
  );
}
