import React, { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "./AccountButton.css";

export default function AccountButton() {
  const { user, login, logout } = useAuth();
  const navigate = useNavigate();
  const [open, setOpen]       = useState(false);
  const [showLogin, setShowLogin] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError]     = useState("");
  const [loading, setLoading] = useState(false);
  const dropRef = useRef(null);

  // Close dropdown on outside click
  useEffect(() => {
    const handler = (e) => {
      if (dropRef.current && !dropRef.current.contains(e.target)) setOpen(false);
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(username, password);
      setShowLogin(false);
      setOpen(false);
      setUsername("");
      setPassword("");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    setOpen(false);
    navigate("/");
  };

  return (
    <div className="account-wrap" ref={dropRef}>
      <button
        className="account-btn"
        onClick={() => setOpen(!open)}
        aria-label="Account"
      >
        <span className="account-avatar">
          {user ? user.username[0].toUpperCase() : "👤"}
        </span>
        <span className="account-label">
          {user ? user.username : "Account"}
        </span>
        <svg className={`account-caret${open ? " open" : ""}`} viewBox="0 0 24 24" width="14" height="14" fill="currentColor">
          <path d="M7 10l5 5 5-5z"/>
        </svg>
      </button>

      {open && !showLogin && (
        <div className="account-dropdown">
          {user ? (
            <>
              <div className="dropdown-user">
                <div className="dropdown-avatar">{user.username[0].toUpperCase()}</div>
                <div>
                  <div className="dropdown-name">{user.username}</div>
                  <div className="dropdown-role">{user.is_admin ? "Administrator" : "User"}</div>
                </div>
              </div>
              <div className="dropdown-divider" />
              {user.is_admin && (
                <button className="dropdown-item admin-item" onClick={() => { navigate("/admin-dashboard"); setOpen(false); }}>
                  <span>⚙️</span> Admin Dashboard
                </button>
              )}
              <button className="dropdown-item logout-item" onClick={handleLogout}>
                <span>🚪</span> Log Out
              </button>
            </>
          ) : (
            <>
              <div className="dropdown-header">Welcome back</div>
              <button className="dropdown-item" onClick={() => { setShowLogin(true); setError(""); }}>
                <span>��</span> Log In
              </button>
            </>
          )}
        </div>
      )}

      {open && showLogin && (
        <div className="account-dropdown login-panel">
          <button className="login-back" onClick={() => setShowLogin(false)}>← Back</button>
          <h3 className="login-title">Sign In</h3>
          <p className="login-sub">Admin or user account</p>
          <form onSubmit={handleLogin} className="login-form" autoComplete="off">
            <div className="login-field">
              <label>Username</label>
              <input
                type="text"
                value={username}
                onChange={e => setUsername(e.target.value)}
                placeholder="Enter username"
                required
                autoFocus
                autoComplete="username"
              />
            </div>
            <div className="login-field">
              <label>Password</label>
              <input
                type="password"
                value={password}
                onChange={e => setPassword(e.target.value)}
                placeholder="Enter password"
                required
                autoComplete="current-password"
              />
            </div>
            {error && <div className="login-error">{error}</div>}
            <button type="submit" className="login-submit" disabled={loading}>
              {loading ? "Signing in…" : "Sign In"}
            </button>
          </form>
        </div>
      )}
    </div>
  );
}
