import React, { useEffect } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
  useLocation,
} from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import { ProductProvider } from "./context/ProductContext";
import Header from "./components/Header";
import Footer from "./components/Footer";
import ProductsPage from "./pages/ProductsPage";
import AboutPage from "./pages/AboutPage";
import ContactPage from "./pages/ContactPage";
import AdminDashboard from "./pages/admin/AdminDashboard";
import WhatsAppFloat from "./components/WhatsAppFloat";
import "./App.css";

function ScrollManager() {
  const { pathname, hash } = useLocation();

  useEffect(() => {
    if (hash) {
      setTimeout(() => {
        const element = document.getElementById(hash.replace("#", ""));
        if (element) {
          element.scrollIntoView({ behavior: "smooth" });
        }
      }, 100);
    } else {
      window.scrollTo({ top: 0, left: 0, behavior: "auto" });
    }
  }, [pathname, hash]);

  return null;
}

function AdminRoute({ children }) {
  const { user, loading } = useAuth();
  if (loading) return null;
  if (!user || !user.is_admin) return <Navigate to="/" replace />;
  return children;
}

function AppRoutes() {
  return (
    <Routes>
      <Route
        path="/"
        element={
          <>
            <Header />
            <main>
              <ProductsPage />
            </main>
            <Footer />
            <WhatsAppFloat />
          </>
        }
      />
      <Route
        path="/about"
        element={
          <>
            <Header />
            <main>
              <AboutPage />
            </main>
            <Footer />
            <WhatsAppFloat />
          </>
        }
      />
      <Route
        path="/contact"
        element={
          <>
            <Header />
            <main>
              <ContactPage />
            </main>
            <Footer />
            <WhatsAppFloat />
          </>
        }
      />
      <Route path="/products" element={<Navigate to="/" replace />} />
      <Route
        path="/admin-dashboard"
        element={
          <AdminRoute>
            <AdminDashboard />
          </AdminRoute>
        }
      />
    </Routes>
  );
}

function App() {
  useEffect(() => {
    const wakeUpBackend = async () => {
      try {
        const API_URL =
          process.env.REACT_APP_API_URL || "http://localhost:8000/api";
        await fetch(`${API_URL}/products/?page_size=1`);
      } catch (error) {
        console.log("Waking up server in background...");
      }
    };

    wakeUpBackend();

    const interval = setInterval(wakeUpBackend, 600000);

    return () => clearInterval(interval);
  }, []);

  return (
    <AuthProvider>
      <ProductProvider>
        <Router>
          <ScrollManager />
          <AppRoutes />
        </Router>
      </ProductProvider>
    </AuthProvider>
  );
}

export default App;
