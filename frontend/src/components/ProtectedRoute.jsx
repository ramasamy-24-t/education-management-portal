import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../hooks/useAuth.js";

export default function ProtectedRoute({ roles, children }) {
  const { user, ready } = useAuth();
  const location = useLocation();

  if (!ready) {
    return <p className="p-6 text-sm text-slate-600">Restoring session…</p>;
  }

  if (!user) {
    const adminOnly = roles?.length === 1 && roles[0] === "admin";
    return <Navigate to={adminOnly ? "/admin/login" : "/login"} replace state={{ from: location }} />;
  }

  if (roles && !roles.includes(user.role)) {
    return <Navigate to="/" replace />;
  }

  return children;
}
