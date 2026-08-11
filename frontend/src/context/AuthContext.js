import React, { createContext, useContext, useState, useEffect, useCallback } from "react";

const API = process.env.REACT_APP_API_URL || "http://localhost:8000/api";
const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser]     = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchMe = useCallback(async (token) => {
    try {
      const res = await fetch(`${API}/auth/me/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) {
        const data = await res.json();
        setUser(data);
      } else {
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        setUser(null);
      }
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const token = localStorage.getItem("access");
    if (token) fetchMe(token);
    else setLoading(false);
  }, [fetchMe]);

  const login = async (username, password) => {
    const res = await fetch(`${API}/auth/login/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Invalid credentials");
    }
    const { access, refresh } = await res.json();
    localStorage.setItem("access", access);
    localStorage.setItem("refresh", refresh);
    await fetchMe(access);
    return access;
  };

  const logout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    setUser(null);
  };

  const getToken = () => localStorage.getItem("access");

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, getToken }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
