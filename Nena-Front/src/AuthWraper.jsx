import { useEffect } from "react";
import { useNavigate } from "react-router";
import { jwtDecode } from 'jwt-decode';
import axios from "axios";


const AuthWrapper = ({ children, Sidebar }) => {
  const token = localStorage.getItem("token");
  const isAuthenticated = !!token;
  const decodedToken = token ? jwtDecode(token) : null;
  const navigate = useNavigate();
  

  useEffect(() => {
    if (!isAuthenticated ) {
        navigate("/signin");
    }
  // Optional: check expiration
  if (decodedToken && decodedToken.exp * 1000 < Date.now()) {
    console.log("Token expired, redirecting to login");
    navigate("/signin");
  }
}, [isAuthenticated, navigate, decodedToken]);

  return (
    <div>
      {Sidebar && <Sidebar />}
      {children}
    </div>
  );
};

export default AuthWrapper;