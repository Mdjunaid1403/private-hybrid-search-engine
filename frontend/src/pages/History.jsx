import { useState, useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
// import { useEffect } from "react";
// import Navigation from "../components/Navigation";


function History()
{

// function History({ setTabs, activeTabId }) {
    // useEffect(() => {
    //     setTabs((currentTabs) =>
    //         currentTabs.map((tab) =>
    //             tab.id === activeTabId
    //                 ? {
    //                     ...tab,
    //                     title: "Search History",
    //                     query: "",
    //                     url: "/history"
    //                 }
    //                 : tab
    //         )
    //     );
    // }, [activeTabId, setTabs]);

    const navigate = useNavigate();
    const { user } = useContext(AuthContext);

    const historyKey = user?.id
        ? `searchHistory_${user.id}`
        : null;

    const [history, setHistory] = useState(() => {
        if (!historyKey) {
            return [];
        }

        return JSON.parse(
            localStorage.getItem(historyKey) || "[]"
        );
    });

    const removeHistoryItem = (indexToRemove) => {
        const updatedHistory = history.filter(
            (_, index) => index !== indexToRemove
        );

        setHistory(updatedHistory);

        if (historyKey)
        {
            localStorage.setItem(
                historyKey,
                JSON.stringify(updatedHistory)
            );
        }
    };

    return (
        <main>
            {/* <Navigation /> */}

            <section className="history-section">
                <h2>Search History</h2>

                {history.length > 0 ? (
                    <ul className="history-list">
                        {history.map((item, index) => (
                            <li
                                key={index}
                                onClick={() => {
                                    navigate(`/search?q=${encodeURIComponent(item)}`);
                                }}
                            >
                                <span>{item}</span>

                                <button
                                    className="history-delete-button"
                                    onClick={(event) => {
                                        event.stopPropagation();
                                        removeHistoryItem(index);
                                    }}
                                >
                                    ×
                                </button>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>No search history yet.</p>
                )}

                {history.length > 0 && (
                    <button
                        onClick={() => {
                            if (historyKey)
                            {
                                localStorage.removeItem(historyKey);
                            }
                            setHistory([]);
                        }}
                    >
                        Clear History
                    </button>
                )}
            </section>
        </main>
    );
}

export default History;