import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';

const ProductContext = createContext();

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const BASE_TAXONOMY = {
  "BEST SELLERS": [
    "Gemstone Bracelets",
    "Tumbled Stones",
    "Pyramid Stone",
    "Gemstone Tree",
    "Selenite Stone",
    "Orgone Pyramid",
    "Healing Crystals",
    "Chips",
    "CHIPS"
  ],
  "SPIRITUAL & HEALING": [
    "Rudraksha",
    "Gemstone Angels",
    "Unique Products",
    "Jap Mala",
    "Fancy Product",
    "Crystal Shivling",
    "Hangings",
    "HANGINGS"
  ],
  "HOME & DECOR": [
    "Rough Stone",
    "Gemstone Ball",
    "Crystal Flowers",
    "Zibu Coins",
    "Tortoise",
    "TORTOISE"
  ],
  "JEWELRY & ACCESSORIES": [
    "Beads String 8mm",
    "Gemstone Pendant",
    "Pendants",
    "Palm Stone",
    "Gemstone",
    "Crystal Heart Stone",
    "Crystal Rakhi",
    "Roller And Guasha",
    "Tumbled Bracelets",
    "Anklets",
    "Bracelet Chip",
    "Ring",
    "ANKLET",
    "BRACELET CHIP",
    "RING"
  ]
};

const DB_TO_DISPLAY_CATEGORY = {
  "TREE": "Gemstone Tree",
  "TUMBLE STONE": "Tumbled Stones",
  "PYRAMIDS": "Pyramid Stone",
  "SELENITE PRODUCTS": "Selenite Stone",
  "CHIPS": "CHIPS",
  "HANGINGS": "HANGINGS",
  "ROUGH": "Rough Stone",
  "ZIBU COINS": "Zibu Coins",
  "TORTOISE": "TORTOISE",
  "PEDANTS": "Gemstone Pendant",
  "RING": "RING",
  "BRACELET CHIP": "BRACELET CHIP",
  "ANKLET": "ANKLET",
  "Gemstone Bracelets": "Gemstone Bracelets"
};

export function ProductProvider({ children }) {
  const [products, setProducts] = useState([]);
  const [fetching, setFetching] = useState(true);
  const [error, setError] = useState(null);
  const [taxonomy, setTaxonomy] = useState(BASE_TAXONOMY);

  const loadProducts = useCallback(async () => {
    setFetching(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/products/?page_size=200&ordering=name`);
      if (!res.ok) throw new Error("Failed to fetch products");
      const data = await res.json();
      const items = data.results || data;
      setProducts(items);

      // Build dynamic taxonomy
      const dynamicTax = {};
      Object.keys(BASE_TAXONOMY).forEach(col => {
        dynamicTax[col] = [...BASE_TAXONOMY[col]];
      });

      items.forEach(p => {
        if (!p.category) return;
        const col = p.collection || "BEST SELLERS";
        if (!dynamicTax[col]) {
          dynamicTax[col] = [];
        }
        
        // Map database raw code to display name if mapped, otherwise use raw category value
        const cleanName = DB_TO_DISPLAY_CATEGORY[p.category] || p.category;
        
        // Check if category is already in the taxonomy collection (case-insensitive)
        const exists = dynamicTax[col].some(cat => cat.toLowerCase() === cleanName.toLowerCase());
        if (!exists) {
          dynamicTax[col].push(cleanName);
        }
      });

      setTaxonomy(dynamicTax);
    } catch (err) {
      console.error("Product fetch error:", err);
      setError(err.message || "Failed to fetch products");
    } finally {
      setFetching(false);
    }
  }, []);

  useEffect(() => {
    loadProducts();
  }, [loadProducts]);

  return (
    <ProductContext.Provider value={{ products, fetching, error, taxonomy, refreshProducts: loadProducts }}>
      {children}
    </ProductContext.Provider>
  );
}

export function useProducts() {
  const context = useContext(ProductContext);
  if (!context) {
    throw new Error("useProducts must be used within a ProductProvider");
  }
  return context;
}
