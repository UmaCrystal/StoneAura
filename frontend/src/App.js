import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
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

function AdminRoute({ children }) {
  const { user, loading } = useAuth();
  if (loading) return null;
  if (!user || !user.is_admin) return <Navigate to="/" replace />;
  return children;
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={
        <>
          <Header />
          <main><ProductsPage /></main>
          <Footer />
          <WhatsAppFloat />
        </>
      } />
      <Route path="/about" element={
        <>
          <Header />
          <main><AboutPage /></main>
          <Footer />
          <WhatsAppFloat />
        </>
      } />
      <Route path="/contact" element={
        <>
          <Header />
          <main><ContactPage /></main>
          <Footer />
          <WhatsAppFloat />
        </>
      } />
      <Route path="/products" element={<Navigate to="/" replace />} />
      <Route path="/admin-dashboard" element={
        <AdminRoute>
          <AdminDashboard />
        </AdminRoute>
      } />
    </Routes>
  );
}

function App() {
  return (
    <AuthProvider>
      <ProductProvider>
        <Router>
          <AppRoutes />
        </Router>
      </ProductProvider>
    </AuthProvider>
  );
}

export default App;
