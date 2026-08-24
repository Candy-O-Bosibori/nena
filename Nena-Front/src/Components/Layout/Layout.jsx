import { useState, useEffect } from 'react';
import { FaBars, FaTimes } from "react-icons/fa";

export const Layout = ({ Sidebar, children }) => {
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);
    const [isLargeScreen, setIsLargeScreen] = useState(
        typeof window !== "undefined" ? window.innerWidth >= 1024 : true
    );
    // The nav rail only makes sense once there's an account to navigate
    // between pages of -- an anonymous visitor on the landing page gets the
    // Sign in button instead (rendered by the page itself).
    const showSidebar = Boolean(Sidebar) && typeof window !== "undefined" && !!localStorage.getItem("access_token");

    useEffect(() => {
        const handleResize = () => setIsLargeScreen(window.innerWidth >= 1024);
        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    // Close the drawer whenever we grow into the desktop layout.
    useEffect(() => {
        if (isLargeScreen) setIsSidebarOpen(false);
    }, [isLargeScreen]);

    return (
        <div className="relative min-h-screen bg-cream lg:flex">
            {/* Mobile menu toggle */}
            {showSidebar && !isLargeScreen && (
                <button
                    onClick={() => setIsSidebarOpen((open) => !open)}
                    aria-label={isSidebarOpen ? "Close menu" : "Open menu"}
                    className="fixed right-4 top-4 z-30 flex h-10 w-10 items-center justify-center rounded-full border border-line bg-surface text-ink shadow-sm transition-colors hover:bg-cream focus-ring"
                >
                    {isSidebarOpen ? <FaTimes size={15} /> : <FaBars size={15} />}
                </button>
            )}

            {/* Backdrop for the mobile drawer */}
            {showSidebar && !isLargeScreen && isSidebarOpen && (
                <div
                    onClick={() => setIsSidebarOpen(false)}
                    className="fixed inset-0 z-10 bg-ink/30 backdrop-blur-sm"
                    aria-hidden="true"
                />
            )}

            {/* Sidebar: fixed rail on desktop, slide-over drawer on mobile */}
            {showSidebar && (
                <aside
                    className={[
                        "z-20 w-64 shrink-0 transition-transform duration-300",
                        isLargeScreen
                            ? "fixed inset-y-0 left-0"
                            : `fixed inset-y-0 left-0 ${isSidebarOpen ? "translate-x-0" : "-translate-x-full"}`,
                    ].join(" ")}
                >
                    <Sidebar />
                </aside>
            )}

            {/* Content */}
            <main className={`min-w-0 flex-1 ${showSidebar ? "lg:ml-64" : ""}`}>
                {children}
            </main>
        </div>
    );
}
