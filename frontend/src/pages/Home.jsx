// import { searchDocuments } from "../api";
// import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import "../App.css";
import ResultCard from "../components/ResultCard";
import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";

function Home({ updateActiveTab }) {

    const navigate = useNavigate();
    const { user } = useContext(AuthContext);

    const [hasSearched, setHasSearched] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [showMenu, setShowMenu] = useState(false);
    const [query, setQuery] = useState("");


    return (
        <>
            <main>
                <section className="search-section">
                    {/* <h1>Search Your Documents</h1> */}

                    {/* <p>
                        Find information quickly from your private local documents.
                    </p> */}

                    <form
                        className="search-box"
                        onSubmit={(event) => {
                            event.preventDefault();

                            if (!query.trim()) {
                                return;
                            }

                            const searchQuery = query.trim();

                            const historySettingKey = `saveSearchHistory_${user.id}`;

                            const saveHistory =
                                localStorage.getItem(historySettingKey) !== "false";

                            if (saveHistory && user?.id) {
                                const historyKey = `searchHistory_${user.id}`;

                                const existingHistory = JSON.parse(
                                    localStorage.getItem(historyKey) || "[]"
                                );

                                const updatedHistory = [
                                    searchQuery,
                                    ...existingHistory.filter(
                                        (item) => item !== searchQuery
                                    )
                                ];

                                localStorage.setItem(
                                    historyKey,
                                    JSON.stringify(updatedHistory)
                                );
                            }

                            updateActiveTab(
                                searchQuery,
                                `/search?q=${encodeURIComponent(searchQuery)}`
                            );

                            navigate(
                                `/search?q=${encodeURIComponent(searchQuery)}`
                            );
                        }}
                    >
                        <input
                            type="text"
                            placeholder="Enter your search query"
                            value={query}
                            onChange={(event) => setQuery(event.target.value)}
                        />

                        <button type="submit">
                            Search
                        </button>
                    </form>
                </section>

                {isLoading && (
                    <p className="loading-message">
                        Searching your documents...
                    </p>
                )}

                {hasSearched && (
                    <section className="results-section">
                        <h2>Search Results</h2>

                        <div className="results-container">
                            {results.length > 0 ? (
                                results.map((result) => (
                                    <ResultCard
                                        key={result.filename}
                                        filename={result.filename}
                                        score={result.score}
                                        preview={result.preview}
                                    />
                                ))
                            ) : (
                                <p className="no-results">
                                    No documents found.
                                </p>
                            )}
                        </div>
                    </section>
                )}

            </main>
        </>
    );
}

export default Home;