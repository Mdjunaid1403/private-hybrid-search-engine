// import Navigation from "../components/Navigation";
// import { useEffect } from "react";
import { useState, useContext } from "react";
import { AuthContext } from "../context/AuthContext";

function Settings() {
// function Settings({ setTabs, activeTabId }) {

    // useEffect(() => {
    //     setTabs((currentTabs) =>
    //         currentTabs.map((tab) =>
    //             tab.id === activeTabId
    //                 ? {
    //                     ...tab,
    //                     title: "Settings",
    //                     query: "",
    //                     url: "/settings"
    //                 }
    //                 : tab
    //         )
    //     );
    // }, [activeTabId, setTabs]);

    const { user } = useContext(AuthContext);

    const [darkMode, setDarkMode] = useState(
        localStorage.getItem("darkMode") === "true"
    );

    const historySettingKey = user?.id
        ? `saveSearchHistory_${user.id}`
        : null;

    const [saveHistory, setSaveHistory] = useState(() => {
        if (!historySettingKey) {
            return true;
        }

        return localStorage.getItem(historySettingKey) !== "false";
    });

    return (
        <main className={darkMode ? "dark-mode" : ""}>
            {/* <Navigation /> */}

            <section className="settings-section">
                <h2>Settings</h2>

                <div className="setting-card">
                    <h3>Search Settings</h3>

                    <p>
                        Configure how search results are displayed.
                    </p>

                    <div className="setting-option">
                        <h4>Search Mode</h4>

                        <select
                            defaultValue={
                                localStorage.getItem("searchMode") || "private-web"
                            }
                            onChange={(event) => {
                                localStorage.setItem(
                                    "searchMode",
                                    event.target.value
                                );
                            }}
                        >
                            <option value="private-web">
                                Private + Web
                            </option>

                            <option value="private-only">
                                Private Documents Only
                            </option>

                            <option value="web-only">
                                Web Only
                            </option>
                        </select>
                    </div>


                    <div className="setting-option">
                        <h4>Results Per Page</h4>

                        <select
                            defaultValue={
                                localStorage.getItem("resultsPerPage") || "10"
                            }
                            onChange={(event) => {
                                localStorage.setItem(
                                    "resultsPerPage",
                                    event.target.value
                                );
                            }}
                        >
                            <option value="5">5 results</option>
                            <option value="10">10 results</option>
                            <option value="15">15 results</option>
                            <option value="20">20 results</option>
                        </select>
                    </div>
                </div>

                <div className="setting-card">
                    <h3>Appearance</h3>

                    <div className="setting-option dark-mode-option">
                        <span>Dark Mode</span>

                        <label className="toggle">
                            <input
                                type="checkbox"
                                checked={darkMode}
                                onChange={(event) => {
                                    const enabled = event.target.checked;

                                    setDarkMode(enabled);
                                    localStorage.setItem(
                                        "darkMode",
                                        enabled.toString()
                                    );

                                    window.dispatchEvent(
                                        new Event("darkModeChange")
                                    );
                                }}
                            />

                            <span className="toggle-slider"></span>
                        </label>
                    </div>
                </div>

                <div className="setting-card">
                    <h3>Search History</h3>

                    <p>
                        Control whether your searches are saved in Search History.
                    </p>

                    <div className="setting-option dark-mode-option">
                        <span>Save Search History</span>

                        <label className="toggle">
                            <input
                                type="checkbox"
                                checked={saveHistory}
                                onChange={(event) => {
                                    const enabled = event.target.checked;

                                    setSaveHistory(enabled);

                                    if (historySettingKey)
                                    {
                                        localStorage.setItem(
                                            "saveSearchHistory",
                                            enabled.toString()
                                        );
                                    }
                                }}
                            />

                            <span className="toggle-slider"></span>
                        </label>
                    </div>
                </div>
            </section>
        </main>
    );
}

export default Settings;