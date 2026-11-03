import {
    BrowserRouter,
    Routes,
    Route,
    useLocation
} from "react-router-dom";

import { useState, useEffect } from "react";
import { useContext } from "react";
import { AuthContext } from "./context/AuthContext";

import Home from "./pages/Home";
import SearchResults from "./pages/SearchResults";
import History from "./pages/History";
import Documents from "./pages/Documents";
import Settings from "./pages/Settings";
import About from "./pages/About";
import DocumentView from "./pages/DocumentView";

import Header from "./components/Header";
import TabBar from "./components/TabBar";

import Login from "./pages/Login";
import Register from "./pages/Register";
import ForgotPassword from "./pages/ForgotPassword";
import ResetPassword from "./pages/ResetPassword";

import ProtectedRoute from "./components/ProtectedRoute";


function RouteTabSync({
    tabs,
    setTabs,
    activeTabId,
    setActiveTabId
}) {
    const location = useLocation();

    useEffect(() => {
        const currentUrl =
            location.pathname + location.search;

        const matchingTab = tabs.find(
            (tab) =>
                tab.url === currentUrl ||
                (tab.searchUrl && tab.searchUrl === currentUrl)
        );

        if (matchingTab && matchingTab.id !== activeTabId) {
            setActiveTabId(matchingTab.id);
        }
    }, [
        location.pathname,
        location.search,
        setActiveTabId
    ]);

    return null;
}

function App() {
    const {
        user,
        isAuthenticated
    } = useContext(AuthContext);

    const [loginMessage, setLoginMessage] = useState("");

    const [darkMode, setDarkMode] = useState(
        localStorage.getItem("darkMode") === "true"
    );


    const [tabs, setTabs] = useState(() => {
        const savedTabs =
            localStorage.getItem("searchTabs");

        if (savedTabs) {
            return JSON.parse(savedTabs);
        }

        return [
            {
                id: 1,
                title: "New Tab",
                query: "",
                url: "/",
                searchUrl: "",
                type: "page"
            }
        ];
    });


    const [activeTabId, setActiveTabId] = useState(() => {
        const savedActiveTab =
            localStorage.getItem("activeTabId");

        return savedActiveTab
            ? Number(savedActiveTab)
            : 1;
    });


    // Save tabs
    useEffect(() => {
        localStorage.setItem(
            "searchTabs",
            JSON.stringify(tabs)
        );
    }, [tabs]);


    // Save active tab
    useEffect(() => {
        localStorage.setItem(
            "activeTabId",
            activeTabId.toString()
        );
    }, [activeTabId]);


    // Update current search tab
    const updateActiveTab = (query, url) => {
        setTabs((currentTabs) =>
            currentTabs.map((tab) =>
                tab.id === activeTabId
                    ? {
                        ...tab,
                        title: query,
                        query: query,
                        url: url,
                        searchUrl: url,
                        type: "search"
                    }
                    : tab
            )
        );
    };


    // Dark mode listener
    useEffect(() => {
        const handleStorageChange = () => {
            setDarkMode(
                localStorage.getItem("darkMode") === "true"
            );
        };

        window.addEventListener(
            "darkModeChange",
            handleStorageChange
        );

        return () => {
            window.removeEventListener(
                "darkModeChange",
                handleStorageChange
            );
        };
    }, []);


    useEffect(() => {
        if (!user) {
            return;
        }

        setLoginMessage(
            `Logged in as: ${user.email}`
        );

        const timer = setTimeout(() => {
            setLoginMessage("");
        }, 2000);

        return () => {
            clearTimeout(timer);
        };
    }, [user]);


    return (

        <BrowserRouter>

            <RouteTabSync
                tabs={tabs}
                setTabs={setTabs}
                activeTabId={activeTabId}
                setActiveTabId={setActiveTabId}
            />

            <div
                className={
                    darkMode
                        ? "app dark-mode"
                        : "app"
                }
            >

                <TabBar
                    tabs={tabs}
                    setTabs={setTabs}
                    activeTabId={activeTabId}
                    setActiveTabId={setActiveTabId}
                />

                <Header
                    user={user}
                    isAuthenticated={isAuthenticated}
                    tabs={tabs}
                    setTabs={setTabs}
                    activeTabId={activeTabId}
                    setActiveTabId={setActiveTabId}
                />

                {loginMessage && (
                    <div className="login-notification">
                        ✓ {loginMessage}
                    </div>
                )}

                {/* {user && (
                    <p>
                        Logged in as: {user.email}
                        {" | "}
                        Authenticated: {isAuthenticated ? "Yes" : "No"}
                    </p>
                )} */}

                <Routes>

                    <Route
                        path="/"
                        element={
                            <ProtectedRoute>
                                <Home
                                    updateActiveTab={
                                        updateActiveTab
                                    }
                                />
                            </ProtectedRoute>
                        }
                    />

                    <Route
                        path="/search"
                        element={
                            <ProtectedRoute>
                                <SearchResults
                                    setTabs={setTabs}
                                    setActiveTabId={
                                        setActiveTabId
                                    }
                                />
                            </ProtectedRoute>
                        }
                    />

                    <Route
                        path="/history"
                        element={
                            <ProtectedRoute>
                                <History />
                            </ProtectedRoute>
                        }
                    />

                    <Route
                        path="/documents"
                        element={
                            <ProtectedRoute>
                                <Documents
                                    setTabs={setTabs}
                                    setActiveTabId={
                                        setActiveTabId
                                    }
                                />
                            </ProtectedRoute>
                        }
                    />

                    <Route
                        path="/documents/:documentId"
                        element={
                            <ProtectedRoute>
                                <DocumentView />
                            </ProtectedRoute>
                        }
                    />

                    <Route
                        path="/settings"
                        element={
                            <ProtectedRoute>
                                <Settings />
                            </ProtectedRoute>
                        }
                    />

                    <Route
                        path="/about"
                        element={
                            <ProtectedRoute>
                                <About />
                            </ProtectedRoute>
                        }
                    />

                    <Route
                        path="/login"
                        element={<Login />}
                    />

                    <Route
                        path="/forgot-password"
                        element={<ForgotPassword />}
                    />

                    <Route
                        path="/register"
                        element={<Register />}
                    />

                    <Route
                        path="/reset-password"
                        element={<ResetPassword />}
                    />

                </Routes>

            </div>

        </BrowserRouter>
    );
}

export default App;