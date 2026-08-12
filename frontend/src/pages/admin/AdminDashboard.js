import React, { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { FaGem, FaHome, FaSignOutAlt, FaSearch, FaStar, FaArrowDown, FaArrowUp, FaEdit, FaTrash, FaUpload, FaImage, FaCheckCircle, FaTimesCircle } from "react-icons/fa";
import { useAuth } from "../../context/AuthContext";
import "./AdminDashboard.css";

const API = process.env.REACT_APP_API_URL || "http://localhost:8000/api";

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

const EMPTY = {
  name: "", price: "", stone_type: "", material: "",
  bead_size: "", color: "", gender: "", shape: "",
  size_info: "", image_url: "", collection: "BEST SELLERS", category: "Gemstone Bracelets", is_featured: false,
};

export default function AdminDashboard() {
  const { user, loading, getToken, logout } = useAuth();
  const navigate = useNavigate();

  const [products, setProducts]   = useState([]);
  const [fetching, setFetching]   = useState(true);
  const [search, setSearch]       = useState("");
  const [view, setView]           = useState("grid"); // grid | form
  const [editing, setEditing]     = useState(null);   // null=new, obj=edit
  const [form, setForm]           = useState(EMPTY);
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const [saving, setSaving]       = useState(false);
  const [toast, setToast]         = useState(null);
  const [deleteId, setDeleteId]   = useState(null);
  const [stats, setStats]         = useState({ total: 0, featured: 0, minPrice: 0, maxPrice: 0 });
  const [currentPage, setCurrentPage] = useState(1);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const PAGE_SIZE = 10;

  // Redirect if not admin
  useEffect(() => {
    if (!loading && (!user || !user.is_admin)) navigate("/");
  }, [user, loading, navigate]);

  const showToast = (msg, type = "success") => {
    setToast({ msg, type });
    setTimeout(() => setToast(null), 3000);
  };

  const fetchProducts = useCallback(async () => {
    setFetching(true);
    try {
      const res = await fetch(`${API}/products/?page_size=100&ordering=name`);
      const data = await res.json();
      const items = data.results || data;
      setProducts(items);
      setStats({
        total: items.length,
        featured: items.filter(p => p.is_featured).length,
        minPrice: Math.min(...items.map(p => parseFloat(p.price))),
        maxPrice: Math.max(...items.map(p => parseFloat(p.price))),
      });
    } catch { showToast("Failed to load products", "error"); }
    finally { setFetching(false); }
  }, []);

  useEffect(() => { fetchProducts(); }, [fetchProducts]);

  const filtered = products.filter(p =>
    p.name.toLowerCase().includes(search.toLowerCase()) ||
    (p.stone_type || "").toLowerCase().includes(search.toLowerCase())
  );

  // Pagination
  const totalPages  = Math.ceil(filtered.length / PAGE_SIZE);
  const paginated   = filtered.slice((currentPage - 1) * PAGE_SIZE, currentPage * PAGE_SIZE);
  const handleSearchChange = (e) => { setSearch(e.target.value); setCurrentPage(1); };

  const openNew = () => {
    setEditing(null);
    setForm(EMPTY);
    setSelectedFile(null);
    setPreviewUrl("");
    setView("form");
  };
  const openEdit = (p) => {
    setEditing(p);
    setForm({
      name: p.name, price: p.price, stone_type: p.stone_type || "",
      material: p.material || "", bead_size: p.bead_size || "",
      color: p.color || "", gender: p.gender || "", shape: p.shape || "",
      size_info: p.size_info || "", image_url: p.image_url || "",
      collection: p.collection || "BEST SELLERS",
      category: p.category || "Gemstone Bracelets", is_featured: p.is_featured,
    });
    setSelectedFile(null);
    setPreviewUrl("");
    setView("form");
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm(f => {
      const updated = { ...f, [name]: type === "checkbox" ? checked : value };
      if (name === "collection") {
        updated.category = TAXONOMY[value]?.[0] || "";
      }
      return updated;
    });
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
    }
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    const token = getToken();
    const method = editing ? "PUT" : "POST";
    const url    = editing ? `${API}/products/${editing.id}/` : `${API}/products/`;

    // Create FormData for multipart submission (supporting files)
    const formData = new FormData();
    Object.keys(form).forEach(key => {
      if (key === "is_featured") {
        formData.append(key, form[key] ? "true" : "false");
      } else if (key === "price") {
        formData.append(key, parseFloat(form[key]));
      } else if (form[key] !== null && form[key] !== undefined) {
        formData.append(key, form[key]);
      }
    });

    if (selectedFile) {
      formData.append("image", selectedFile);
    }

    try {
      const res = await fetch(url, {
        method,
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(JSON.stringify(err));
      }
      showToast(editing ? "Bracelet updated!" : "Bracelet added!");
      await fetchProducts();
      setView("grid");
    } catch (err) {
      showToast(err.message || "Save failed", "error");
    } finally { setSaving(false); }
  };

  const handleDelete = async (id) => {
    const token = getToken();
    try {
      const res = await fetch(`${API}/products/${id}/`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error("Delete failed");
      showToast("Bracelet deleted");
      setDeleteId(null);
      await fetchProducts();
    } catch { showToast("Delete failed", "error"); }
  };

  const toggleFeatured = async (p) => {
    const token = getToken();
    try {
      await fetch(`${API}/products/${p.id}/`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
        body: JSON.stringify({ is_featured: !p.is_featured }),
      });
      await fetchProducts();
    } catch { showToast("Update failed", "error"); }
  };

  if (loading || fetching) return (
    <div className="admin-loading">
      <div className="admin-spinner"></div>
      <p>Loading dashboard…</p>
    </div>
  );

  return (
    <div className="admin-page">
      {/* MOBILE TOP BAR */}
      <div className="admin-mobile-header">
        <a href="/" className="sidebar-logo">
          <div className="sidebar-logo-icon"><FaGem /></div>
          <div>
            <div className="sidebar-brand">Aurastone</div>
            <div className="sidebar-sub">Admin Panel</div>
          </div>
        </a>
        <button className="admin-hamburger" onClick={() => setSidebarOpen(true)} aria-label="Open menu">
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>

      {/* OVERLAY BACKDROP */}
      {sidebarOpen && (
        <div className="admin-sidebar-overlay" onClick={() => setSidebarOpen(false)} />
      )}

      {/* SIDEBAR */}
      <aside className={`admin-sidebar${sidebarOpen ? " open" : ""}`}>
        <button className="admin-sidebar-close" onClick={() => setSidebarOpen(false)} aria-label="Close menu">✕</button>
        <div className="sidebar-logo">
          <div className="sidebar-logo-icon"><FaGem /></div>
          <div>
            <div className="sidebar-brand">Aurastone</div>
            <div className="sidebar-sub">Admin Panel</div>
          </div>
        </div>
        <nav className="sidebar-nav">
          <button className={`sidebar-item active`} onClick={() => setSidebarOpen(false)}>
            <FaGem className="sidebar-icon-react" /> Bracelets
          </button>
          <button className="sidebar-item" onClick={() => { setSidebarOpen(false); navigate("/"); }}>
            <FaHome className="sidebar-icon-react" /> View Store
          </button>
          <button className="sidebar-item logout" onClick={() => { setSidebarOpen(false); logout(); navigate("/"); }}>
            <FaSignOutAlt className="sidebar-icon-react" /> Log Out
          </button>
        </nav>
        <div className="sidebar-footer">
          <div className="sidebar-user-chip">
            <div className="sidebar-avatar">{user?.username?.[0]?.toUpperCase()}</div>
            <div>
              <div className="sidebar-uname">{user?.username}</div>
              <div className="sidebar-urole">Administrator</div>
            </div>
          </div>
        </div>
      </aside>

      {/* MAIN */}
      <main className="admin-main">
        {/* TOP BAR */}
        <div className="admin-topbar">
          <div>
            <h1 className="admin-title">{view === "form" ? (editing ? "Edit Bracelet" : "Add New Bracelet") : "Bracelet Management"}</h1>
            <p className="admin-sub">{view === "form" ? "Fill in the details below" : `Showing ${paginated.length} of ${filtered.length} bracelets`}</p>
          </div>
          <div className="topbar-actions">
            {view === "grid" ? (
              <button className="btn-add" onClick={openNew}>
                <span>+</span> Add Bracelet
              </button>
            ) : (
              <button className="btn-back" onClick={() => setView("grid")}>
                ← Back to List
              </button>
            )}
          </div>
        </div>

        {view === "grid" && (
          <>
            {/* STATS */}
            <div className="admin-stats">
              {[
                { icon: <FaGem />, label: "Total Bracelets", value: stats.total },
                { icon: <FaStar />, label: "Featured",        value: stats.featured },
                { icon: <FaArrowDown />, label: "Lowest Price",    value: `₹${stats.minPrice}` },
                { icon: <FaArrowUp />, label: "Highest Price",   value: `₹${stats.maxPrice}` },
              ].map(s => (
                <div key={s.label} className="stat-card">
                  <div className="stat-card-icon">{s.icon}</div>
                  <div className="stat-card-value">{s.value}</div>
                  <div className="stat-card-label">{s.label}</div>
                </div>
              ))}
            </div>

            {/* SEARCH */}
            <div className="admin-search-bar">
              <span><FaSearch /></span>
              <input
                type="search"
                placeholder="Search by name or stone type…"
                value={search}
                onChange={e => handleSearchChange(e)}
              />
            </div>

            {/* PRODUCT TABLE */}
            <div className="admin-table-wrap">
              <table className="admin-table">
                <thead>
                  <tr>
                    <th>Image</th>
                    <th>Name</th>
                    <th>Stone Type</th>
                    <th>Price</th>
                    <th>Featured</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {paginated.map(p => (
                    <tr key={p.id}>
                      <td>
                        <img
                          src={p.image_url}
                          alt={p.name}
                          className="table-img"
                          onError={e => { e.target.src = "https://via.placeholder.com/60x45?text=No+Img"; }}
                        />
                      </td>
                      <td className="table-name">
                        <div>{p.name}</div>
                        <div style={{ fontSize: "0.75rem", color: "var(--text-light)", marginTop: "2px" }}>
                          {p.collection} &rsaquo; {p.category}
                        </div>
                      </td>
                      <td><span className="stone-chip">{p.stone_type || "—"}</span></td>
                      <td className="table-price">₹{p.price}</td>
                      <td>
                        <button
                          className={`featured-toggle${p.is_featured ? " on" : ""}`}
                          onClick={() => toggleFeatured(p)}
                          title={p.is_featured ? "Remove from featured" : "Mark as featured"}
                        >
                          {p.is_featured ? <><FaStar /> Yes</> : <><FaStar style={{ opacity: 0.3 }} /> No</>}
                        </button>
                      </td>
                      <td className="table-actions">
                        <button className="btn-edit" onClick={() => openEdit(p)}><FaEdit /> Edit</button>
                        <button className="btn-delete" onClick={() => setDeleteId(p.id)}><FaTrash /> Delete</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* PAGINATION */}
            {totalPages > 1 && (
              <div className="pagination-bar">
                <button
                  className="page-btn prev"
                  onClick={() => setCurrentPage(p => Math.max(p - 1, 1))}
                  disabled={currentPage === 1}
                >
                  ← Previous
                </button>

                <div className="page-numbers">
                  {Array.from({ length: totalPages }, (_, i) => i + 1).map(n => (
                    <button
                      key={n}
                      className={`page-num${currentPage === n ? " active" : ""}`}
                      onClick={() => setCurrentPage(n)}
                    >
                      {n}
                    </button>
                  ))}
                </div>

                <button
                  className="page-btn next"
                  onClick={() => setCurrentPage(p => Math.min(p + 1, totalPages))}
                  disabled={currentPage === totalPages}
                >
                  Next →
                </button>
              </div>
            )}
          </>
        )}

        {view === "form" && (
          <form className="admin-form" onSubmit={handleSave}>
            <div className="form-grid">
              {/* LEFT: Image Preview */}
              <div className="form-preview">
                {previewUrl ? (
                  <img src={previewUrl} alt="Preview" />
                ) : form.image_url ? (
                  <img src={form.image_url} alt="Preview" onError={e => { e.target.style.display="none"; }} />
                ) : (
                  <div className="preview-placeholder">
                    <span><FaImage /></span>
                    <p>Select an image to see preview</p>
                  </div>
                )}
                <div className="form-price-badge">₹{form.price || "0"}</div>
              </div>

              {/* RIGHT: Fields */}
              <div className="form-fields">
                <div className="form-row two">
                  <div className="form-group">
                    <label>Bracelet Name *</label>
                    <input name="name" value={form.name} onChange={handleChange} placeholder="e.g. Rose Quartz Bracelet" required />
                  </div>
                  <div className="form-group">
                    <label>Price (₹) *</label>
                    <input name="price" type="number" min="1" value={form.price} onChange={handleChange} placeholder="e.g. 299" required />
                  </div>
                </div>

                <div className="form-row two">
                  <div className="form-group">
                    <label>Stone Type</label>
                    <input name="stone_type" value={form.stone_type} onChange={handleChange} placeholder="e.g. Amethyst" />
                  </div>
                  <div className="form-group">
                    <label>Material</label>
                    <input name="material" value={form.material} onChange={handleChange} placeholder="e.g. Natural Stone" />
                  </div>
                </div>

                <div className="form-row three">
                  <div className="form-group">
                    <label>Bead Size</label>
                    <input name="bead_size" value={form.bead_size} onChange={handleChange} placeholder="e.g. 8 mm" />
                  </div>
                  <div className="form-group">
                    <label>Color</label>
                    <input name="color" value={form.color} onChange={handleChange} placeholder="e.g. Purple" />
                  </div>
                  <div className="form-group">
                    <label>Gender</label>
                    <input name="gender" value={form.gender} onChange={handleChange} placeholder="e.g. Unisex" />
                  </div>
                </div>

                <div className="form-row two">
                  <div className="form-group">
                    <label>Shape</label>
                    <input name="shape" value={form.shape} onChange={handleChange} placeholder="e.g. Oval, Round" />
                  </div>
                  <div className="form-group">
                    <label>Size Info</label>
                    <input name="size_info" value={form.size_info} onChange={handleChange} placeholder="e.g. Free, 7 Inch" />
                  </div>
                </div>

                <div className="form-group full">
                  <label>Bracelet Image</label>
                  <div className="upload-container">
                    <label className="upload-box-btn">
                      <span className="upload-box-icon"><FaUpload /></span>
                      <span className="upload-box-text">
                        {selectedFile ? selectedFile.name : (form.image_url ? "Change Image File" : "Choose Image File")}
                      </span>
                      <input 
                        type="file" 
                        accept="image/*" 
                        onChange={handleFileChange} 
                        style={{ display: "none" }} 
                      />
                    </label>
                    {form.image_url && !selectedFile && (
                      <span className="current-image-path">Current Path: {form.image_url}</span>
                    )}
                  </div>
                </div>

                <div className="form-row two">
                  <div className="form-group">
                    <label>Collection</label>
                    <select name="collection" value={form.collection} onChange={handleChange}>
                      {Object.keys(TAXONOMY).map(col => (
                        <option key={col} value={col}>{col}</option>
                      ))}
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Category</label>
                    <select name="category" value={form.category} onChange={handleChange}>
                      {(TAXONOMY[form.collection] || []).map(cat => (
                        <option key={cat} value={cat}>{cat}</option>
                      ))}
                    </select>
                  </div>
                </div>
                <div className="form-row two">
                  <div className="form-group featured-check">
                    <label className="checkbox-label">
                      <input type="checkbox" name="is_featured" checked={form.is_featured} onChange={handleChange} />
                      <span>Mark as Featured</span>
                    </label>
                  </div>
                  <div className="form-group"></div>
                </div>

                <div className="form-actions">
                  <button type="button" className="btn-cancel" onClick={() => setView("grid")}>Cancel</button>
                  <button type="submit" className="btn-save" disabled={saving}>
                    {saving ? "Saving…" : (editing ? "Update Bracelet" : "Add Bracelet")}
                  </button>
                </div>
              </div>
            </div>
          </form>
        )}
      </main>

      {/* DELETE CONFIRM MODAL */}
      {deleteId && (
        <div className="confirm-overlay" onClick={() => setDeleteId(null)}>
          <div className="confirm-box" onClick={e => e.stopPropagation()}>
            <div className="confirm-icon"><FaTrash /></div>
            <h3>Delete Bracelet?</h3>
            <p>This action cannot be undone.</p>
            <div className="confirm-btns">
              <button className="btn-cancel" onClick={() => setDeleteId(null)}>Cancel</button>
              <button className="btn-confirm-delete" onClick={() => handleDelete(deleteId)}>Delete</button>
            </div>
          </div>
        </div>
      )}

      {/* TOAST */}
      {toast && (
        <div className={`admin-toast ${toast.type}`}>
          {toast.type === "success" ? <FaCheckCircle /> : <FaTimesCircle />} {toast.msg}
        </div>
      )}
    </div>
  );
}
