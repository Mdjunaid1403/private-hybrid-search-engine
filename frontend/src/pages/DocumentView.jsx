import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getDocument } from "../api";

function DocumentView() {
    const { documentId } = useParams();

    const [document, setDocument] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        getDocument(documentId)
            .then((data) => {
                setDocument(data);
            })
            .catch((error) => {
                console.error(
                    "Failed to load document:",
                    error
                );

                setError(error.message);
            })
            .finally(() => {
                setLoading(false);
            });
    }, [documentId]);

    if (loading) {
        return (
            <main>
                <section className="document-view-section">
                    <p>Loading document...</p>
                </section>
            </main>
        );
    }

    if (error) {
        return (
            <main>
                <section className="document-view-section">
                    <p>{error}</p>
                </section>
            </main>
        );
    }

    return (
        <main>
            <section className="document-view-section">

                <h2>{document.filename}</h2>

                <div className="document-content">
                    <pre>{document.content}</pre>
                </div>

            </section>
        </main>
    );
}

export default DocumentView;