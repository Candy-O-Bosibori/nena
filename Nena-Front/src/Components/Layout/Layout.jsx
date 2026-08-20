import { useState, useEffect } from 'react';
import { FaBars, FaTimes } from "react-icons/fa";

export const Layout = ({ Sidebar, children }) => {
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);
    const [isLargeScreen, setIsLargeScreen] = useState(window.innerWidth >= 1024);

    const handleSidebarToggle = () => {
        setIsSidebarOpen(!isSidebarOpen);
    };

    useEffect(() => {
        const handleResize = () => {
            setIsLargeScreen(window.innerWidth >= 1024);
        };

        window.addEventListener('resize', handleResize);
        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, []);

    return (
        <div className={`relative h-screen overflow-auto ${isLargeScreen ? 'flex' : ''}`}>
            <button onClick={handleSidebarToggle} className="absolute right-0 z-20 p-3 lg:hidden">
                {isSidebarOpen ? <FaTimes className='fill-black'/> : <FaBars className='fill-black' />}
            </button>
            {(isSidebarOpen || isLargeScreen) && (
                <div className={`z-10 w-full lg:w-64 bg-white ${isLargeScreen ? 'fixed top-0 left-0 h-screen w-64' : 'absolute w-full'}`}>
                    {Sidebar && <Sidebar />}
                </div>
            )}
            {!isSidebarOpen || isLargeScreen ? (
                <div className={`flex-grow  ${isLargeScreen ? "lg:ml-64 h-screen" : ""}`}>
               
                  {children}
                </div>
            ) : null}
        </div>
    );
}
