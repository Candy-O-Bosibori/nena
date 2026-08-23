import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Details } from "./Details";
import { jwtDecode } from "jwt-decode";
import { toast } from "react-toastify";
import { FiLogOut } from "react-icons/fi";
import api from "../../api/api";
import ThemeToggle from "../../Components/ui/ThemeToggle";

export const Profile = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState({});
  const [showNameModal, setShowNameModal] = useState(false);
  const [userNameData, setUsernameData] = useState({ username: "" });
  const [showEmailModal, setShowEmailModal] = useState(false);
  const [email, setEmail] = useState({ email: "" });
  const [showPasswordModal, setShowPasswordModal] = useState(false);
  const [password, setPassword] = useState({
    current: "",
    newpassword: "",
    confirmpassword: "",
  });
  const [submitting, setSubmitting] = useState(false);

  const getUserId = () => {
    const token = localStorage.getItem("access_token");
    if (!token) return null;
    try {
      const decoded = jwtDecode(token);
      return decoded?.sub?.id ?? decoded?.sub;
    } catch {
      return null;
    }
  };

  useEffect(() => {
    const userId = getUserId();
    if (!userId) return;

    api
      .get(`/userById/${userId}`)
      .then(({ data }) => setUser(data))
      .catch((err) => {
        console.error(err);
        toast.error("Failed to load profile");
      });
  }, []);

  const handleUsernameChange = (e) => {
    const { id, value } = e.target;
    setUsernameData((prev) => ({ ...prev, [id]: value }));
  };

  const handlePasswordChange = (e) => {
    const { id, value } = e.target;
    setPassword((prev) => ({ ...prev, [id]: value }));
  };

  const handleEmailChange = (e) => {
    const { id, value } = e.target;
    setEmail((prev) => ({ ...prev, [id]: value }));
  };

  const handleSignOut = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refreshToken");
    navigate("/signin");
  };

  const handleSubmitUsername = async (e) => {
    e.preventDefault();
    const userId = getUserId();
    if (!userId) return;

    setSubmitting(true);
    try {
      const { data } = await api.patch(`/userById/${userId}`, {
        name: userNameData.username,
      });
      setUser(data.user);
      setShowNameModal(false);
      setUsernameData({ username: "" });
      toast.success("Name successfully changed");
    } catch (err) {
      toast.error(err.response?.data?.error || "Failed to update name");
    } finally {
      setSubmitting(false);
    }
  };

  const handleSubmitEmail = async (e) => {
    e.preventDefault();
    const userId = getUserId();
    if (!userId) return;

    setSubmitting(true);
    try {
      const { data } = await api.patch(`/userById/${userId}`, {
        email: email.email,
      });
      setUser(data.user);
      setShowEmailModal(false);
      setEmail({ email: "" });
      toast.success("Email successfully changed");
    } catch (err) {
      toast.error(err.response?.data?.error || "Failed to update email");
    } finally {
      setSubmitting(false);
    }
  };

  const handleSubmitPassword = async (e) => {
    e.preventDefault();
    const userId = getUserId();
    if (!userId) return;

    if (!password.current) {
      toast.error("Enter your current password");
      return;
    }
    if (!password.newpassword || password.newpassword !== password.confirmpassword) {
      toast.error("New password and confirmation must match");
      return;
    }

    setSubmitting(true);
    try {
      await api.patch(`/userById/${userId}`, {
        current_password: password.current,
        newpassword: password.newpassword,
      });
      setShowPasswordModal(false);
      setPassword({ current: "", newpassword: "", confirmpassword: "" });
      toast.success("Password successfully changed");
    } catch (err) {
      toast.error(err.response?.data?.error || "Failed to change password");
    } finally {
      setSubmitting(false);
    }
  };

  let content;

  if (showNameModal) {
    content = (
      <div className="fixed inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm z-50">
        <div className="bg-surface p-4 rounded shadow-lg max-w-full w-[350px] lg:w-[500px]">
          <h2 className="mb-2 text-center font-display text-2xl font-normal text-ink">
            Change Name
          </h2>
          <form onSubmit={handleSubmitUsername}>
            <textarea
              id="username"
              value={userNameData.username}
              onChange={handleUsernameChange}
              className="w-full mb-2 rounded-xl border border-line bg-cream px-4 py-2.5 text-sm text-ink transition-colors focus:border-primary focus:bg-surface focus:outline-none"
            ></textarea>
            <div className="flex justify-end gap-2">
              <button
                type="button"
                onClick={() => setShowNameModal(false)}
                className="rounded-xl border border-line bg-surface px-4 py-2 text-sm font-semibold text-ink-soft transition-colors hover:text-ink"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={submitting}
                className="rounded-xl bg-primary px-4 py-2 text-sm font-bold text-on-primary transition-all duration-200 hover:bg-primary-hover active:scale-[0.98] disabled:opacity-60"
              >
                Submit
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  } else if (showEmailModal) {
    content = (
      <div className="fixed inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm z-50">
        <div className="bg-surface p-4 rounded shadow-lg max-w-full w-[350px] lg:w-[500px]">
          <h2 className="mb-2 text-center font-display text-2xl font-normal text-ink">
            Change Email
          </h2>
          <form onSubmit={handleSubmitEmail}>
            <textarea
              id="email"
              value={email.email}
              onChange={handleEmailChange}
              className="w-full mb-2 rounded-xl border border-line bg-cream px-4 py-2.5 text-sm text-ink transition-colors focus:border-primary focus:bg-surface focus:outline-none"
            ></textarea>
            <div className="flex justify-end gap-2">
              <button
                type="button"
                onClick={() => setShowEmailModal(false)}
                className="rounded-xl border border-line bg-surface px-4 py-2 text-sm font-semibold text-ink-soft transition-colors hover:text-ink"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={submitting}
                className="rounded-xl bg-primary px-4 py-2 text-sm font-bold text-on-primary transition-all duration-200 hover:bg-primary-hover active:scale-[0.98] disabled:opacity-60"
              >
                Submit
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  } else if (showPasswordModal) {
    content = (
      <div className="fixed inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm z-50">
        <div className="bg-surface p-4 rounded shadow-lg max-w-full w-[350px] lg:w-[500px]">
          <h2 className="mb-2 text-center font-display text-2xl font-normal text-ink">
            Change Password
          </h2>
          <form onSubmit={handleSubmitPassword}>
            <label className="block mb-2 text-sm text-ink-soft" htmlFor="current">
              Current Password
              <input
                id="current"
                type="password"
                autoComplete="current-password"
                value={password.current}
                onChange={handlePasswordChange}
                className="w-full mt-1 rounded-xl border border-line bg-cream px-4 py-2.5 text-sm text-ink transition-colors focus:border-primary focus:bg-surface focus:outline-none"
              />
            </label>
            <label className="block mb-2 text-sm text-ink-soft" htmlFor="newpassword">
              New Password
              <input
                id="newpassword"
                type="password"
                autoComplete="new-password"
                value={password.newpassword}
                onChange={handlePasswordChange}
                className="w-full mt-1 rounded-xl border border-line bg-cream px-4 py-2.5 text-sm text-ink transition-colors focus:border-primary focus:bg-surface focus:outline-none"
              />
            </label>
            <label className="block mb-2 text-sm text-ink-soft" htmlFor="confirmpassword">
              Confirm Password
              <input
                id="confirmpassword"
                type="password"
                autoComplete="new-password"
                value={password.confirmpassword}
                onChange={handlePasswordChange}
                className="w-full mt-1 rounded-xl border border-line bg-cream px-4 py-2.5 text-sm text-ink transition-colors focus:border-primary focus:bg-surface focus:outline-none"
              />
            </label>

            <div className="flex justify-end gap-2 mt-2">
              <button
                type="button"
                onClick={() => setShowPasswordModal(false)}
                className="rounded-xl border border-line bg-surface px-4 py-2 text-sm font-semibold text-ink-soft transition-colors hover:text-ink"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={submitting}
                className="rounded-xl bg-primary px-4 py-2 text-sm font-bold text-on-primary transition-all duration-200 hover:bg-primary-hover active:scale-[0.98] disabled:opacity-60"
              >
                Submit
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  } else {
    content = (
      <Details
        user={user}
        setShowNameModal={setShowNameModal}
        setShowPasswordModal={setShowPasswordModal}
        setShowEmailModal={setShowEmailModal}
      />
    );
  }

  return (
    <div className="min-h-screen bg-cream">
      <div className="mx-auto w-full max-w-4xl px-5 py-10">
        {/* heading */}
        <header className="mb-8">
          <h1 className="font-display text-3xl font-normal tracking-tight text-ink md:text-4xl">Your Profile</h1>
          <p className="mt-2 text-sm text-ink-soft">Manage your profile and preferences.</p>
        </header>

        <div className="flex flex-col gap-6">
          <div>{content}</div>

          {/* Preferences */}
          <div className="rounded-2xl border border-line bg-surface px-5 py-4">
            <h2 className="mb-3 text-[11px] font-bold uppercase tracking-[0.16em] text-ink-muted">
              Preferences
            </h2>
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-ink">Theme</span>
              <ThemeToggle />
            </div>
          </div>

          {/* Session */}
          <div className="rounded-2xl border border-line bg-surface px-5 py-4">
            <h2 className="mb-3 text-[11px] font-bold uppercase tracking-[0.16em] text-ink-muted">
              Session
            </h2>
            <button
              onClick={handleSignOut}
              className="flex items-center gap-2 rounded-xl px-3 py-2.5 text-sm font-semibold text-danger transition-colors hover:bg-danger/10 focus-ring"
            >
              <FiLogOut className="h-4 w-4" />
              Sign out
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
