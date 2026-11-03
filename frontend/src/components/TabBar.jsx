import { useNavigate, useLocation } from "react-router-dom";
import { useEffect } from "react";

function TabBar({
    tabs,
    setTabs,
    activeTabId,
    setActiveTabId
}) {
    const navigate = useNavigate();
    const location = useLocation();

    /*Update the title of the active PAGE tab
      based on the current URL.

      Document tabs are protected so their
      filename is never replaced.*/

    useEffect(() => {

        // Individual document page
        // Never change the title of a document tab.
        if (
            location.pathname.startsWith("/documents/")
        ) {
            return;
        }

        const activeTab = tabs.find(
            (tab) => tab.id === activeTabId
        );

        if (!activeTab) {
            return;
        }

        const currentUrl =
            location.pathname + location.search;

        if (
            activeTab.url !== currentUrl &&
            activeTab.searchUrl !== currentUrl
        ) {
            return;
        }

        setTabs((currentTabs) =>
            currentTabs.map((tab) => {

                if (tab.id !== activeTabId) {
                    return tab;
                }

                // If this is a document tab,
                // never change its filename.
                if (tab.type === "document") {
                    return tab;
                }

                // Documents page
                if (location.pathname === "/documents") {
                    return {
                        ...tab,
                        type: "page",
                        title: "Documents",
                        url: "/documents",
                        searchUrl: ""
                    };
                }

                // Search page
                if (location.pathname === "/search") {

                    const params = new URLSearchParams(
                        location.search
                    );

                    const query = params.get("q");

                    return {
                        ...tab,
                        type: "search",
                        title: query || "Search",
                        query: query || "",
                        url:
                            location.pathname +
                            location.search,
                        searchUrl:
                            location.pathname +
                            location.search
                    };
                }

                // Search History
                if (location.pathname === "/history") {
                    return {
                        ...tab,
                        type: "page",
                        title: "Search History",
                        url: "/history",
                        searchUrl: ""
                    };
                }

                // Settings
                if (location.pathname === "/settings") {
                    return {
                        ...tab,
                        type: "page",
                        title: "Settings",
                        url: "/settings",
                        searchUrl: ""
                    };
                }

                // About
                if (location.pathname === "/about") {
                    return {
                        ...tab,
                        type: "page",
                        title: "About",
                        url: "/about",
                        searchUrl: ""
                    };
                }

                // Home
                if (location.pathname === "/") {
                    return {
                        ...tab,
                        type: "page",
                        title: "New Tab",
                        query: "",
                        url: "/",
                        searchUrl: ""
                    };
                }

                return tab;
            })
        );

    }, [
        location.pathname,
        location.search,
        activeTabId,
        setTabs
    ]);


    const handleTabClick = (tab) => {

        setActiveTabId(tab.id);

        if (tab.searchUrl) {
            navigate(tab.searchUrl);
        } else {
            navigate(tab.url || "/");
        }
    };


    const handleCloseTab = (event, tab) => {

        event.stopPropagation();

        const updatedTabs = tabs.filter(
            (item) => item.id !== tab.id
        );


        // If this is the last tab
        if (updatedTabs.length === 0) {

            const newTab = {
                id: Date.now(),
                title: "New Tab",
                query: "",
                url: "/",
                searchUrl: "",
                type: "page"
            };

            setTabs([newTab]);
            setActiveTabId(newTab.id);
            navigate("/");

            return;
        }


        // Closing a non-active tab
        if (tab.id !== activeTabId) {

            setTabs(updatedTabs);

            return;
        }


        // Closing active tab
        const closedTabIndex = tabs.findIndex(
            (item) => item.id === tab.id
        );


        const previousTab =
            tabs[closedTabIndex - 1] ||
            updatedTabs[0];


        setTabs(updatedTabs);
        setActiveTabId(previousTab.id);


        if (previousTab.searchUrl) {
            navigate(previousTab.searchUrl);
        } else {
            navigate(previousTab.url || "/");
        }
    };


    const handleNewTab = () => {

        const newTab = {
            id: Date.now(),
            title: "New Tab",
            query: "",
            url: "/",
            searchUrl: "",
            type: "page"
        };

        setTabs((currentTabs) => [
            ...currentTabs,
            newTab
        ]);

        setActiveTabId(newTab.id);

        navigate("/");
    };


    return (
        <div className="tab-bar">

            {tabs.map((tab) => (

                <div
                    className={
                        tab.id === activeTabId
                            ? "tab active-tab"
                            : "tab"
                    }
                    key={tab.id}
                    onClick={() =>
                        handleTabClick(tab)
                    }
                >

                    <span>
                        {tab.title ||
                            tab.query ||
                            "New Tab"}
                    </span>


                    <button
                        type="button"
                        onClick={(event) =>
                            handleCloseTab(
                                event,
                                tab
                            )
                        }
                    >
                        ×
                    </button>

                </div>

            ))}


            <button
                type="button"
                className="new-tab-button"
                onClick={handleNewTab}
            >
                +
            </button>

        </div>
    );
}

export default TabBar;