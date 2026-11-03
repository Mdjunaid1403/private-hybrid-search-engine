import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getDocuments, uploadDocument, deleteDocument } from "../api";

function Documents({
    setTabs,
    setActiveTabId
}) {
    const navigate = useNavigate();

    const [documents, setDocuments] = useState([]);
    const [documentToDelete, setDocumentToDelete] = useState(null);
    const [deleteError, setDeleteError] = useState("");
    const [selectedFile, setSelectedFile] = useState(null);
    const [uploadMessage, setUploadMessage] = useState("");

    useEffect(() => {
        getDocuments()
            .then((data) => {
                setDocuments(data.documents);
            })
            .catch((error) => {
                console.error(
                    "Failed to load documents:",
                    error
                );
            });
    }, []);

    const handleUpload = () => {
        if (!selectedFile) {
            setUploadMessage(
                "Please select a file."
            );
            return;
        }

        uploadDocument(selectedFile)
            .then(() => {
                setUploadMessage(
                    "File uploaded successfully."
                );

                setSelectedFile(null);

                return getDocuments();
            })
            .then((data) => {
                setDocuments(data.documents);
            })
            .catch((error) => {
                setUploadMessage(error.message);
            });
    };


    const handleDelete = async () => {
        if (!documentToDelete) {
            return;
        }

        const { id } = documentToDelete;

        setDeleteError("");

        try {
            await deleteDocument(id);

            setDocuments((currentDocuments) =>
                currentDocuments.filter(
                    (document) => document.id !== id
                )
            );

            setDocumentToDelete(null);
        } catch (error) {
            console.error("Failed to delete document:", error);

            setDeleteError(
                error.message || "Failed to delete document."
            );
        }
    };

    const openDocument = (document) => {
        const newTab = {
            id: Date.now(),
            title: document.filename,
            query: "",
            url: `/documents/${document.id}`,
            searchUrl: "",
            type: "document"
        };

        setTabs((currentTabs) => [
            ...currentTabs,
            newTab
        ]);

        setActiveTabId(newTab.id);

        navigate(`/documents/${document.id}`);
    };

    return (
        <main>
            <section className="documents-section">

                <div className="upload-section">

                    <p className="supported-file-types">
                        Supported files: TXT, PDF, DOCX, PPTX, XLSX, CSV, MD, HTML, ZIP
                    </p>

                    <input
                        type="file"
                        accept=".txt, .pdf, .docx, .pptx, .xlsx, .csv, .md, .html, .zip"
                        onChange={(event) => {
                            setSelectedFile(
                                event.target.files[0]
                            );
                        }}
                    />

                    <button
                        type="button"
                        onClick={handleUpload}
                    >
                        Upload
                    </button>

                    {uploadMessage && (
                        <p>{uploadMessage}</p>
                    )}

                </div>

                <h2>Your Documents</h2>

                <p>
                    Your indexed documents will appear here.
                </p>

                <div className="documents-list">

                    {documents.map((document) => (

                        <div
                            className="document-item"
                            key={document.id}
                        >

                            <button
                                type="button"
                                onClick={() =>
                                    openDocument(document)
                                }
                            >
                                {document.filename}
                            </button>

                            <button
                                type="button"
                                onClick={() => {
                                    setDeleteError("");
                                    setDocumentToDelete({
                                        id: document.id,
                                        filename: document.filename
                                    });
                                }}
                            >
                                Delete
                            </button>

                        </div>

                    ))}

                </div>

            </section>

            {documentToDelete && (
                <div className="delete-modal-overlay">
                    <div
                        className="delete-modal"
                        role="dialog"
                        aria-modal="true"
                        aria-labelledby="delete-modal-title"
                    >
                        <h2 id="delete-modal-title">
                            Delete Document
                        </h2>

                        <p>
                            Are you sure you want to delete{" "}
                            <strong>
                                {documentToDelete.filename}
                            </strong>
                            ?
                        </p>

                        <p>This action cannot be undone.</p>

                        {deleteError && (
                            <p className="delete-error">
                                {deleteError}
                            </p>
                        )}

                        <div className="delete-modal-actions">
                            <button
                                type="button"
                                onClick={() => {
                                    setDocumentToDelete(null);
                                    setDeleteError("");
                                }}
                            >
                                Cancel
                            </button>

                            <button
                                type="button"
                                onClick={handleDelete}
                            >
                                Delete
                            </button>
                        </div>
                    </div>
                </div>
            )}

        </main>
    );
}

export default Documents;