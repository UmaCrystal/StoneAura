
import React, { useState, useEffect } from 'react';
import './ProductModal.css';

const WRIST_SIZES = [
  { label: '6mm',  cm: '6 mm beads',  inches: 'Small beads' },
  { label: '8mm',  cm: '8 mm beads',  inches: 'Standard beads' },
  { label: '12mm', cm: '12 mm beads', inches: 'Large beads' },
];

export default function ProductModal({ product, onClose }) {
  const [selectedSize, setSelectedSize] = useState('8mm');
  const [showSizeGuide, setShowSizeGuide] = useState(false);

  useEffect(() => {
    const onKey = (e) => { if (e.key === 'Escape') onClose(); };
    document.addEventListener('keydown', onKey);
    document.body.style.overflow = 'hidden';
    return () => {
      document.removeEventListener('keydown', onKey);
      document.body.style.overflow = '';
    };
  }, [onClose]);

  if (!product) return null;

  const handleQuote = () => {
    const priceText = product.price ? ` priced at ₹${product.price}` : '';
    const sizeText = product.price_unit !== 'per kg' ? ` (Size: ${selectedSize})` : '';
    const msg = encodeURIComponent(
      `Hi, I am interested in ${product.name}${sizeText}${priceText}`
    );
    window.open(`https://wa.me/919104139899?text=${msg}`, '_blank', 'noopener,noreferrer');
  };

  const props = [
    product.stone_type && { key: 'Stone Type', val: product.stone_type },
    product.material   && { key: 'Material',   val: product.material },
    product.bead_size  && { key: 'Bead Size',  val: product.bead_size },
    product.color      && { key: 'Color',      val: product.color },
    product.gender     && { key: 'Gender',     val: product.gender },
    product.shape      && { key: 'Shape',      val: product.shape },
    product.category   && { key: 'Category',   val: product.category },
  ].filter(Boolean);

  return (
    <>
      <div className="modal-overlay open" onClick={onClose} role="dialog" aria-modal="true" aria-label={product.name}>
        <div className="modal" onClick={(e) => e.stopPropagation()}>
          <button className="modal-close" onClick={onClose} aria-label="Close">✕</button>
          <div className="modal-inner">
            {/* LEFT: Image */}
            <div className="modal-image">
              {product.image_url ? (
                <img
                  src={product.image_url}
                  alt={product.name}
                  loading="eager"
                  decoding="async"
                  onError={(e) => { e.target.src = 'https://placehold.co/500x500/f5f0e8/c9a84c?text=StoneAura'; }}
                />
              ) : (
                <div className="img-placeholder" style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f5f0e8' }}>
                  <div className="img-placeholder-inner" style={{ textAlign: 'center' }}>
                    <span className="img-placeholder-gem" style={{ fontSize: '2.5rem' }}>💎</span>
                    <div className="img-placeholder-name" style={{ fontSize: '1rem', color: '#8c763e', marginTop: '8px', fontWeight: '500' }}>{product.stone_type || product.name}</div>
                  </div>
                </div>
              )}
            </div>

            {/* RIGHT: Details */}
            <div className="modal-body">
              {product.stone_type && <div className="modal-stone-type">{product.stone_type}</div>}
              <h2 className="modal-title">{product.name}</h2>
              {product.price ? (
                <div className="modal-price">
                  ₹{product.price} <span className="modal-price-unit">/ {product.price_unit ? product.price_unit.replace('per ', '') : 'piece'}</span>
                </div>
              ) : (
                <div className="modal-price" style={{ color: '#c9a84c' }}>Price on Request</div>
              )}

              {props.length > 0 && (
                <div className="modal-props">
                  {props.map(p => (
                    <div key={p.key} className="modal-prop">
                      <span className="modal-prop-key">{p.key}</span>
                      <span className="modal-prop-val">{p.val}</span>
                    </div>
                  ))}
                </div>
              )}

              {/* Wholesale Pricing Table */}
              {product.price && (
                <div className="modal-pricing">
                  <div className="modal-pricing-title">Wholesale Pricing</div>
                  <table className="pricing-table">
                    <thead>
                      <tr>
                        <th>Qty</th>
                        <th>Price / {product.price_unit ? product.price_unit.replace('per ', '') : 'pc'}</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>1 {product.price_unit ? product.price_unit.replace('per ', '') : 'pc'}</td>
                        <td className="pt-price">₹{product.price}</td>
                      </tr>
                      {product.price_10pc && (
                        <tr>
                          <td>10 {product.price_unit ? product.price_unit.replace('per ', 'pcs') : 'pcs'}</td>
                          <td className="pt-price">₹{product.price_10pc}</td>
                        </tr>
                      )}
                      {product.price_50pc && (
                        <tr>
                          <td>50 {product.price_unit ? product.price_unit.replace('per ', 'pcs') : 'pcs'}</td>
                          <td className="pt-price">₹{product.price_50pc}</td>
                        </tr>
                      )}
                      {product.price_100pc && (
                        <tr>
                          <td>100 {product.price_unit ? product.price_unit.replace('per ', 'pcs') : 'pcs'}</td>
                          <td className="pt-price">₹{product.price_100pc}</td>
                        </tr>
                      )}
                    </tbody>
                  </table>
                </div>
              )}

              {/* Wrist Size Selector */}
              {product.price_unit !== 'per kg' && (
                <div className="modal-size-section">
                  <div className="modal-size-label">
                    Select Bead Size
                    <button className="size-guide-link" onClick={() => setShowSizeGuide(true)}>
                      Size Guide →
                    </button>
                  </div>
                  <div className="modal-sizes">
                    {WRIST_SIZES.map(sz => (
                      <button
                        key={sz.label}
                        className={`modal-size-btn${selectedSize === sz.label ? ' selected' : ''}`}
                        onClick={() => setSelectedSize(sz.label)}
                        title={`${sz.cm} / ${sz.inches}`}
                      >
                        {sz.label}
                      </button>
                    ))}
                  </div>
                  <div className="selected-size-info">
                    {WRIST_SIZES.find(s => s.label === selectedSize)?.cm} &nbsp;·&nbsp;
                    {WRIST_SIZES.find(s => s.label === selectedSize)?.inches}
                  </div>
                </div>
              )}

              <button className="modal-cta" onClick={handleQuote}>
                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                  <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/>
                  <path d="M12 0C5.373 0 0 5.373 0 12c0 2.123.554 4.118 1.528 5.855L0 24l6.335-1.508A11.945 11.945 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.818a9.818 9.818 0 01-5.006-1.371l-.36-.214-3.727.977.994-3.634-.235-.374A9.818 9.818 0 1112 21.818z"/>
                </svg>
                {product.price_unit === 'per kg' ? 'Get Quote on WhatsApp' : `Get Quote on WhatsApp (Size: ${selectedSize})`}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Size Guide Popup */}
      {showSizeGuide && (
        <div className="size-guide-popup open" onClick={() => setShowSizeGuide(false)}>
          <div className="size-guide-box" onClick={(e) => e.stopPropagation()}>
            <h3>Bead Size Guide</h3>
            <p className="sg-tip">Choose the bead size that suits your style and bracelet type.</p>
            <table className="size-table">
              <thead>
                <tr><th>Bead Size</th><th>Description</th><th>Best For</th></tr>
              </thead>
              <tbody>
                {WRIST_SIZES.map(sz => (
                  <tr key={sz.label} className={selectedSize === sz.label ? 'highlighted' : ''}>
                    <td><strong>{sz.label}</strong></td>
                    <td>{sz.cm}</td>
                    <td>{sz.inches}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <button className="sg-close" onClick={() => setShowSizeGuide(false)}>Got it!</button>
          </div>
        </div>
      )}
    </>
  );
}
