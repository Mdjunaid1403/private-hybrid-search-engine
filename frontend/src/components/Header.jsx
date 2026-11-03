import { useState, useContext, useEffect, useRef } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

function Header({
    tabs,
    setTabs,
    activeTabId,
    setActiveTabId
}) {
    const [showMenu, setShowMenu] = useState(false);
    const [showAccountMenu, setShowAccountMenu] = useState(false);
    const navRef = useRef(null);
    const navigate = useNavigate();

    const location = useLocation();

    const navigateToPage = (path, title) => {
        const currentPath = location.pathname;

        if (currentPath === "/")
        {
            setTabs((currentTabs) =>
                currentTabs.map((tab) =>
                    tab.id === activeTabId
                        ? {
                            ...tab,
                            title,
                            query: "",
                            url: path,
                            searchUrl: "",
                            type: "page"
                        }
                        : tab
                )
            );

            navigate(path);
        }
        else
        {
            const newTab = {
                id: Date.now(),
                title,
                query: "",
                url: path,
                searchUrl: "",
                type: "page"
            };

            setTabs((currentTabs) => [
                ...currentTabs,
                newTab
            ]);

            setActiveTabId(newTab.id);
            navigate(path);
        }

        setShowMenu(false);
        setShowAccountMenu(false);
    };


    const {
        user,
        isAuthenticated,
        logout
    } = useContext(AuthContext);

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (navRef.current && !navRef.current.contains(event.target))
            {
                setShowMenu(false);
                setShowAccountMenu(false);
            }
        };

        document.addEventListener(
            "mousedown",
            handleClickOutside
        );

        return () => {
            document.removeEventListener(
                "mousedown",
                handleClickOutside
            );
        };
    }, []);

    return (
        <header className="header">
            <div className="logo">
                Private Search
            </div>

            <nav ref={navRef}>

                <button
                    className="more-button"
                    onClick={() => navigateToPage("/", "Home")}
                >
                    Home
                </button>


                <button
                    className="more-button"
                    onClick={() => navigateToPage("/about", "About")}
                >
                    About
                </button>


                <button
                    className="more-button"
                    onClick={() => {
                        setShowMenu(!showMenu);
                        setShowAccountMenu(false);
                    }}
                >
                    More ⋮
                </button>

                {showMenu && (
                    <div className="more-menu">
                        <button
                            onClick={() => navigateToPage("/history", "Search History")}
                        >
                            Search History
                        </button>

                        <button
                            onClick={() => navigateToPage("/documents", "Documents")}
                        >
                            Documents
                        </button>

                        <button
                            onClick={() => navigateToPage("/settings", "Settings")}
                        >
                            Settings
                        </button>

                        {/* <button
                            onClick={() => {
                                setShowMenu(false);
                                logout();
                                navigate("/login");
                            }}
                        >
                            Logout
                        </button>  */}
                    </div>
                )}

                {isAuthenticated && (
                    <button
                        className="user-button"
                        onClick={() => {
                            setShowAccountMenu(!showAccountMenu);
                            setShowMenu(false);
                        }}
                        title="Account"
                    >
                        👤
                    </button>
                )}

                {isAuthenticated && showAccountMenu && (
                    <div className="account-menu">
                        <div className="account-email">
                            {user.email}
                        </div>

                        <button
                            className="account-logout"
                            onClick={() =>{
                                setShowAccountMenu(false);
                                logout();
                                navigate("/login");
                            }}
                        >
                            Logout
                        </button>
                    </div>
                )}

            </nav>
        </header>
    );
}

export default Header;