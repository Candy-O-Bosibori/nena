import { useState, useEffect, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';
import { PiEyeLight } from "react-icons/pi";
import { PiEyeSlash } from "react-icons/pi";
import logo from "../../assets/logo.png";
import github from "../../assets/github.png";
import google from "../../assets/google.png";
import facebook from "../../assets/facebook.png";
import image from "../../assets/image.png";
import { API_BASE_URL } from "../../utils/apiBase";

export const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();
    const location = useLocation();
    const returnTo = location.state?.returnTo;
    const [passwordVisible, setPasswordVisible] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);


    const togglePasswordVisibility = () => {
        setPasswordVisible(!passwordVisible);
    };

    const refreshToken = useRef(async () => {
        const refreshToken = localStorage.getItem('refreshToken');

        try {
            const response = await fetch(`${API_BASE_URL}/refresh`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${refreshToken}`
                }
            });

            if (!response.ok) {
                throw new Error('Error: ' + response.statusText);
            }

            const data = await response.json();
            localStorage.setItem('access_token', data.access_token);
            if (data.refresh_token) {
                localStorage.setItem('refreshToken', data.refresh_token);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        if (token) {
            try {
                const decodedToken = jwtDecode(token);
                const expiresIn = decodedToken.exp * 1000 - new Date().getTime();
                setTimeout(refreshToken, expiresIn - 60000);
            } catch (error) {
                console.error("Invalid token", error);
            }
        }
    }, []);

    const handleSubmit = async (event) => {
        event.preventDefault();
        setErrorMessage('');
        setIsLoading(true);

        try {
            const response = await fetch(`${API_BASE_URL}/signin`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                }),
            });
            const data = await response.json();

            if (!response.ok) {
                const message = data?.error || 'Invalid email or password';
                setErrorMessage(message);
                setIsLoading(false);
                return;
            }

            
            if (data.access_token) {
                // Saves the access token into the browser’s localStorage so the user stays logged in.
                localStorage.setItem("access_token", data.access_token);
                // used to get new access token later
                localStorage.setItem("refreshToken", data.refresh_token);

                navigate(returnTo || "/overview");

            } else {
                setErrorMessage("Access token is missing in the response");
            }
        } catch (error) {
            console.error("Error:", error);
            setErrorMessage("Something went wrong. Please try again.");
        }
        setIsLoading(false); 
    };

    return (
      <div className="flex min-h-screen items-center justify-center bg-cream px-5 py-10">
        <div className="grid w-full max-w-4xl overflow-hidden rounded-3xl border border-line bg-surface shadow-xl md:grid-cols-2">
          {/* Left side - Login form */}
          <div className="flex flex-col justify-center p-8 md:p-12">
            <img className="mb-8 h-9 w-auto self-start object-contain" src={logo} alt="Nena" />

            <h1 className="font-display text-3xl font-normal tracking-tight text-ink">Welcome back</h1>
            <p className="mt-2 text-sm text-ink-soft">
              Sign in to keep building your speaking confidence.
            </p>

            {errorMessage && (
              <div className="mt-5 rounded-xl border border-danger/20 bg-danger/5 px-4 py-3 text-sm font-medium text-danger">
                {errorMessage}
              </div>
            )}

            {/* Form */}
            <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
              <div>
                <label className="mb-1.5 block text-sm font-semibold text-ink">Email</label>
                <input
                  className="w-full rounded-xl border border-line bg-cream px-4 py-3 text-sm text-ink transition-colors placeholder:text-ink-muted focus:border-primary focus:bg-surface focus:outline-none"
                  type="email"
                  placeholder="you@example.com"
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                />
              </div>

              <div>
                <label className="mb-1.5 block text-sm font-semibold text-ink">Password</label>
                <div className="relative">
                  <input
                    className="w-full rounded-xl border border-line bg-cream px-4 py-3 pr-11 text-sm text-ink transition-colors placeholder:text-ink-muted focus:border-primary focus:bg-surface focus:outline-none"
                    type={passwordVisible ? "text" : "password"}
                    placeholder="Your password"
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                  />
                  <button
                    type="button"
                    onClick={togglePasswordVisibility}
                    aria-label={passwordVisible ? "Hide password" : "Show password"}
                    className="absolute inset-y-0 right-0 flex items-center pr-3.5 text-ink-muted transition-colors hover:text-ink"
                  >
                    {passwordVisible ? <PiEyeLight size={18} /> : <PiEyeSlash size={18} />}
                  </button>
                </div>
              </div>

              <div className="flex items-center justify-between pt-1">
                <label className="flex items-center gap-2 text-sm text-ink-soft">
                  <input type="checkbox" className="h-4 w-4 rounded accent-primary" />
                  Remember me
                </label>
                <button type="button" className="text-sm font-semibold text-primary hover:underline">
                  Forgot password?
                </button>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="flex w-full items-center justify-center gap-2 rounded-xl bg-primary py-3.5 text-sm font-bold text-on-primary shadow-sm transition-all duration-200 hover:bg-primary-hover active:scale-[0.99] disabled:opacity-50 focus-ring"
              >
                {isLoading && (
                  <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/40 border-t-white" />
                )}
                {isLoading ? "Signing in…" : "Sign in"}
              </button>
            </form>

            {/* Divider */}
            <div className="my-6 flex items-center gap-3">
              <div className="h-px flex-1 bg-line" />
              <span className="text-xs font-medium text-ink-muted">or continue with</span>
              <div className="h-px flex-1 bg-line" />
            </div>

            {/* Social login */}
            <button className="flex w-full items-center justify-center gap-2.5 rounded-xl border border-line bg-surface py-3 text-sm font-semibold text-ink transition-colors hover:bg-cream focus-ring">
              <img src={google} alt="" className="h-5 w-5" />
              Google
            </button>

            {/* Register link */}
            <p className="mt-8 text-center text-sm text-ink-soft">
              Don’t have an account?{" "}
              <button
                type="button"
                className="font-bold text-primary hover:underline"
                onClick={() => navigate('/signup', { state: returnTo ? { returnTo } : undefined })}
              >
                Register for free
              </button>
            </p>
          </div>

          {/* Right side - Illustration (hidden on small screens) */}
          <div className="hidden items-center justify-center bg-cream p-12 md:flex">
            <img src={image} alt="" className="max-w-xs" />
          </div>
        </div>
      </div>
    );
}
