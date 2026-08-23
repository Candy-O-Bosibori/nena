import axios from "axios";

let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

const logout = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refreshToken");
  if (!window.location.pathname.startsWith("/signin")) {
    window.location.href = "/signin";
  }
};

const refreshAccessToken = async () => {
  const refreshToken = localStorage.getItem("refreshToken");
  if (!refreshToken) {
    logout();
    return null;
  }

  try {
    // Send the refresh token in the Authorization header (what the server
    // expects); the body is kept as a compatibility fallback.
    const response = await axios.post(
      "http://127.0.0.1:5000/refresh",
      { token: refreshToken },
      { headers: { Authorization: `Bearer ${refreshToken}` } }
    );

    const newAccessToken =
      response.data.access_token || response.data.accessToken;
    if (!newAccessToken) throw new Error("No access token in refresh response");

    localStorage.setItem("access_token", newAccessToken);

    // The server rotates the refresh token, so an active user never expires.
    const rotated = response.data.refresh_token || response.data.refreshToken;
    if (rotated) localStorage.setItem("refreshToken", rotated);

    return newAccessToken;
  } catch (error) {
    // Only sign out when the server actively rejected the refresh token.
    // A network blip or a 5xx must NOT log the user out -- that was the bug
    // where a momentary backend hiccup kicked you back to the login page.
    const status = error.response?.status;
    if (status === 401 || status === 422) {
      logout();
    } else {
      console.warn("Token refresh failed (transient); staying signed in", error);
    }
    return null;
  }
};

const api = axios.create({
  baseURL: "http://127.0.0.1:5000",
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const refreshToken = localStorage.getItem("refreshToken");

    // Only a token-related 401 (flask-jwt-extended's loaders in extensions.py,
    // which all set a "code" like "token_expired") should trigger a
    // refresh-and-retry. A 401 an endpoint returns itself as an application
    // error (e.g. "current password incorrect") has no such code and must
    // surface to the caller instead of silently logging the user out.
    const isAuthError =
      error.response?.status === 401 && error.response?.data?.code !== undefined;

    if (isAuthError && !originalRequest._retry && refreshToken) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then(token => {
            originalRequest.headers["Authorization"] = `Bearer ${token}`;
            return api(originalRequest);
          })
          .catch(err => Promise.reject(err));
      }

      originalRequest._retry = true;
      isRefreshing = true;

      const newAccessToken = await refreshAccessToken();
      if (newAccessToken) {
        api.defaults.headers.common["Authorization"] = `Bearer ${newAccessToken}`;
        originalRequest.headers["Authorization"] = `Bearer ${newAccessToken}`;
        processQueue(null, newAccessToken);
        isRefreshing = false;
        return api(originalRequest);
      } else {
        processQueue(error, null);
        isRefreshing = false;
        return Promise.reject(error);
      }
    }

    return Promise.reject(error);
  }
);

export default api;