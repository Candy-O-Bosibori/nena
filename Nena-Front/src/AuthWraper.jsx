import { useEffect, useState } from "react";
import { useNavigate } from "react-router";
import { jwtDecode } from "jwt-decode";
import axios from "axios";

const API_BASE = "http://127.0.0.1:5000";

// jwtDecode throws on a malformed token; never let that white-screen the app.
const safeDecode = (token) => {
  if (!token) return null;
  try {
    return jwtDecode(token);
  } catch {
    return null;
  }
};

const isExpired = (decoded) => {
  if (!decoded?.exp) return false;
  // 30s skew so we refresh just before the server would reject it.
  return decoded.exp * 1000 < Date.now() + 30_000;
};

const AuthWrapper = ({ children, Sidebar }) => {
  const [isLoading, setIsLoading] = useState(true);
  const [allowed, setAllowed] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    let cancelled = false;

    const signOut = () => {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refreshToken");
      navigate("/signin", { replace: true });
    };

    const initializeAuth = async () => {
      const token = localStorage.getItem("access_token");
      const refreshToken = localStorage.getItem("refreshToken");

      // With no refresh token there is no way back in.
      if (!token && !refreshToken) {
        if (!cancelled) {
          signOut();
          setIsLoading(false);
        }
        return;
      }

      const decoded = safeDecode(token);

      // Valid, unexpired access token: nothing to do.
      if (decoded && !isExpired(decoded)) {
        if (!cancelled) {
          setAllowed(true);
          setIsLoading(false);
        }
        return;
      }

      // Expired or unreadable access token: refresh instead of signing out.
      if (!refreshToken) {
        if (!cancelled) {
          signOut();
          setIsLoading(false);
        }
        return;
      }

      try {
        const res = await axios.post(
          `${API_BASE}/refresh`,
          { token: refreshToken },
          { headers: { Authorization: `Bearer ${refreshToken}` } }
        );

        const newAccessToken = res.data.access_token || res.data.accessToken;
        if (!newAccessToken) throw new Error("No access token in refresh response");

        localStorage.setItem("access_token", newAccessToken);

        const rotated = res.data.refresh_token || res.data.refreshToken;
        if (rotated) localStorage.setItem("refreshToken", rotated);

        if (!cancelled) {
          setAllowed(true);
          setIsLoading(false);
        }
      } catch (error) {
        const status = error.response?.status;
        if (status === 401 || status === 422) {
          // The server actively rejected the refresh token: genuinely signed out.
          if (!cancelled) {
            signOut();
            setIsLoading(false);
          }
        } else {
          // Backend down or network blip. Do NOT sign the user out over this --
          // render the app and let api.js retry on the next request.
          console.warn("Auth refresh failed (transient); staying signed in", error);
          if (!cancelled) {
            setAllowed(true);
            setIsLoading(false);
          }
        }
      }
    };

    initializeAuth();
    return () => {
      cancelled = true;
    };
  }, []);

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center bg-cream text-sm text-ink-muted">
        Loading...
      </div>
    );
  }

  if (!allowed) return null;

  return (
    <div>
      {Sidebar && <Sidebar />}
      {children}
    </div>
  );
};

export default AuthWrapper;
