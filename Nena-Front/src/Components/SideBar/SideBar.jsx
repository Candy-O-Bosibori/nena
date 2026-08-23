import React, { useEffect, useState } from 'react'
import { NavLink } from 'react-router-dom';
import logo from "../../assets/logo.png";
import { jwtDecode } from 'jwt-decode';
import api from '../../api/api';
import { CiHome, CiViewList, CiSettings, CiBookmarkPlus } from "react-icons/ci";

const NAV_ITEMS = [
  { to: "/overview", label: "Practice", Icon: CiHome },
  { to: "/feedback", label: "Feedback", Icon: CiViewList },
  { to: "/vocab", label: "Vocabulary", Icon: CiBookmarkPlus },
  { to: "/profile", label: "Profile", Icon: CiSettings },
];

export const SideBar = () => {
  const [employee, setEmployee] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) return;

    let userId;
    try {
      const decodedToken = jwtDecode(token);
      userId = decodedToken?.sub?.id ?? decodedToken?.sub;
    } catch {
      return; // malformed token: AuthWrapper handles the redirect
    }

    api.get('/users')
      .then(({ data }) => {
        setEmployee(data.find(u => String(u.id) === String(userId)));
      })
      .catch(error => console.error('Error:', error));
  }, []);

  const initials = (employee?.name || "")
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((n) => n[0]?.toUpperCase())
    .join("");

  return (
    <div className="flex h-screen w-full flex-col justify-between border-r border-line bg-cream px-5 py-7">
      <div>
        <div className="flex items-center justify-center px-2">
          <img src={logo} alt="Nena" className="h-9 w-auto object-contain" />
        </div>

        <nav className="mt-10">
          <ul className="flex flex-col gap-1">
            {NAV_ITEMS.map(({ to, label, Icon }) => (
              <li key={to}>
                <NavLink to={to} className="block focus-ring rounded-xl">
                  {({ isActive }) => (
                    <div
                      className={[
                        "flex items-center justify-center gap-3 px-3 py-2.5",
                        "text-sm transition-colors duration-200",
                        isActive
                          ? "text-primary"
                          : "text-ink-soft hover:text-ink",
                      ].join(" ")}
                    >
                      <Icon className="h-5 w-5 shrink-0" />
                      <span>{label}</span>
                    </div>
                  )}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
      </div>

      <div className="flex flex-col gap-3">
        {employee && (
          <div className="flex items-center gap-3 rounded-2xl border border-line bg-surface px-3 py-2.5">
            {employee.image ? (
              <img
                src={employee.image}
                alt={employee.name}
                className="h-9 w-9 shrink-0 rounded-full object-cover"
              />
            ) : (
              <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-primary text-xs font-bold text-on-primary">
                {initials || "?"}
              </span>
            )}
            <div className="min-w-0">
              <p className="truncate text-sm font-semibold text-ink">{employee.name}</p>
              <p className="truncate text-xs text-ink-muted">{employee.email}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
