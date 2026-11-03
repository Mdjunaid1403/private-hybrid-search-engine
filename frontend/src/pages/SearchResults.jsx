import {
    useSearchParams,
    useNavigate
} from "react-router-dom";
import { useState, useEffect } from "react";
import ResultCard from "../components/ResultCard";
import {
    combinedSearchDocuments,
    hybridSearchDocuments,
    webSearchDocuments,
} from "../api";


function SearchResults({
    setTabs,
    setActiveTabId
}) {
    const [searchParams] = useSearchParams();

    const navigate = useNavigate();

    const query = searchParams.get("q") || "";

    const [privateResults, setPrivateResults] = useState([]);
    const [webResults, setWebResults] = useState([]);

    const [isLoading, setIsLoading] = useState(false);

    const [error, setError] = useState("");

    // const [documents, setDocuments] = useState([]);


    // Load document list so search results
    // can be matched with document IDs.
    // useEffect(() => {

    //     getDocuments()
    //         .then((data) => {
    //             setDocuments(data.documents);
    //         })
    //         .catch((error) => {
    //             console.error(
    //                 "Failed to load documents:",
    //                 error
    //             );
    //         });

    // }, []);


    // Perform search
    useEffect(() => {
        let isActive = true;

        if (!query) {
            setPrivateResults([]);
            setWebResults([]);
            setIsLoading(false);
            setError("");
            return;
        }

        setIsLoading(true);
        setError("");

        const searchMode =
            localStorage.getItem("searchMode") || "private-web";

        const resultsPerPage =
            Number(localStorage.getItem("resultsPerPage")) || 10;

        let searchRequest;


        if (searchMode === "private-only")
        {
            searchRequest = hybridSearchDocuments(query);
        }
        else if (searchMode === "web-only")
        {
            searchRequest = webSearchDocuments(query);
        }
        else
        {
            searchRequest = combinedSearchDocuments(query, resultsPerPage);
        }


        searchRequest
            .then((data) => {
                if (!isActive) return;

                if (searchMode === "private-only")
                {
                    setPrivateResults(data.results);
                    setWebResults([]);
                }
                else if (searchMode === "web-only")
                {
                    setPrivateResults([]);
                    setWebResults(data.results);
                }
                else
                {
                    setPrivateResults(data.private_results);

                    if (data.web_results.length > 0)
                    {
                    setWebResults(data.web_results);
                    }
                }

            })
            .catch(() => {
                if(!isActive) return;

                setError("Unable to connect to the search server.");
            })

            .finally(() => {
                if(!isActive) return;

                setIsLoading(false);
            })

            return () => {
                isActive = false;
            };

    }, [query]);


    // Open a private document in a new search tab
    const openDocument = (result) => {

        if (!result.document_id) {
            console.error("Document ID missing:", result);
            return;
        }

        // const document = documents.find(
        //     (item) =>
        //         item.filename === filename
        // );

        // if (!document) {
        //     console.error("Document not found:", filename);
        //     return;
        // }

        const newTab = {
            id: Date.now(),
            title: result.filename,
            query: "",
            url: `/documents/${result.document_id}`,
            searchUrl: "",
            type: "document"
        };


        setTabs((currentTabs) => [
            ...currentTabs,
            newTab
        ]);


        setActiveTabId(newTab.id);

        // window.history.pushState(
        //     {},
        //     "",
        //     `/documents/${document.id}`
        // );

        // window.dispatchEvent(
        //     new PopStateEvent("popstate")
        // );

        navigate(`/documents/${result.document_id}`);
    };


    return (
        <main>

            <section className="results-section">

                <h2>
                    Search Results for "{query}"
                </h2>


                <div className="results-container">

                    {isLoading ? (

                        <p className="loading-message">
                            Searching...
                        </p>

                    ) : error ? (

                        <p className="error-message">
                            {error}
                        </p>

                    ) : (

                        <>

                            <h3>
                                Private Documents
                            </h3>


                            {privateResults.length > 0 ? (

                                privateResults.map(
                                    (result) => (

                                        <div
                                            key={
                                                result.document_id
                                            }
                                            onClick={() =>
                                                openDocument(result)
                                            }
                                            style={{
                                                cursor: "pointer"
                                            }}
                                        >

                                            <ResultCard
                                                filename={
                                                    result.filename
                                                }
                                                keywordScore={
                                                    result.keyword_score
                                                }
                                                semanticScore={
                                                    result.semantic_score
                                                }
                                                hybridScore={
                                                    result.hybrid_score
                                                }
                                            />

                                        </div>

                                    )
                                )

                            ) : (

                                <p className="no-results">
                                    No private documents found.
                                </p>

                            )}


                            <h3>
                                Web Results
                            </h3>


                            {webResults.length > 0 ? (

                                webResults.map(
                                    (result, index) => (

                                        <div
                                            className="result-card"
                                            key={index}
                                        >

                                            <div className="result-header">

                                                <h3>
                                                    {result.title}
                                                </h3>

                                            </div>


                                            <a
                                                href={
                                                    result.href
                                                }
                                                target="_blank"
                                                rel="noopener noreferrer"
                                            >
                                                {
                                                    result.href.length > 60
                                                        ? `${result.href.slice(0, 60)}...`
                                                        : result.href
                                                }
                                            </a>


                                            <p className="result-preview">
                                                {result.body}
                                            </p>

                                        </div>

                                    )
                                )

                            ) : (

                                <p className="no-results">
                                    No web results found.
                                </p>

                            )}
                        </>
                    )}
                </div>
            </section>
        </main>
    );
}

export default SearchResults;