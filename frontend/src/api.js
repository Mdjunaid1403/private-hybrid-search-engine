const API_URL = import.meta.env.VITE_API_URL;

function getAuthToken() {
    return localStorage.getItem("access_token");
}

export async function testApi() {
    try {
        const response = await fetch(`${API_URL}/`);

        if (!response.ok) {
            throw new Error("API request failed");
        }

        const data = await response.json();

        return data;
    } catch (error) {
        console.error("API Error:", error);
        throw error;
    }
}

export async function searchDocuments(query) {
    try {
        const token = getAuthToken();

        const response = await fetch(
            `${API_URL}/search?query=${encodeURIComponent(query)}`,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        if (!response.ok) {
            throw new Error("Search request failed");
        }

        const data = await response.json();

        return data;
    } catch (error) {
        console.error("Search API Error:", error);
        throw error;
    }
}

export async function semanticSearchDocuments(query) {
    try {
        const token = getAuthToken();

        const response = await fetch(
            `${API_URL}/semantic-search?query=${encodeURIComponent(query)}`,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        if (!response.ok) {
            throw new Error("Semantic search request failed");
        }

        const data = await response.json();

        return data;
    } catch (error) {
        console.error("Semantic Search API Error:", error);
        throw error;
    }
}

export async function hybridSearchDocuments(query) {
    try {
        const token = getAuthToken();

        const response = await fetch(
            `${API_URL}/hybrid-search?query=${encodeURIComponent(query)}`,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        if (!response.ok) {
            throw new Error("Hybrid Search request failed");
        }

        const data = await response.json();

        return data;
    } catch (error) {
        console.error("Hybrid Search API Error:", error);
        throw error;
    }
}

export async function combinedSearchDocuments(query, limit = 5) {
    try {
        const token = getAuthToken();

        const response = await fetch(
            `${API_URL}/combined-search?query=${encodeURIComponent(query)}&limit=${limit}`,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
            throw new Error(data.detail || "Search failed. Please try again.");
        }

        return data;
    } catch (error) {
        console.error("Combined Search API Error:", error);

        if (error instanceof TypeError)
        {
            throw new Error("Unable to connect to the server. Please check your connection and try again.")
        }
        throw error;
    }
}

export async function webSearchDocuments(query) {
    try {
        const token = getAuthToken();

        const response = await fetch(
            `${API_URL}/web-search?query=${encodeURIComponent(query)}`,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        if (!response.ok) {
            throw new Error("Web Search request failed");
        }

        const data = await response.json();

        return data;
    } catch (error) {
        console.error("Web Search API Error:", error);
        throw error;
    }
}

export async function getDocuments() {
    try {
        const token = getAuthToken();

        const response = await fetch(`${API_URL}/documents`,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );
        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
            throw new Error(data.detail || "Unable to load your documents. Please try again.");
        }

        return data;
    } catch (error) {
        console.error("Documents API Error:", error);

        if (error instanceof TypeError) {
            throw new Error("Unable to connect to the server. Please check your connection and try again.");
        }
        throw error;
    }
}

export async function getDocument(documentId) {
    try {
        const token = getAuthToken();

        const response = await fetch(
            `${API_URL}/documents/${documentId}`,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );
        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
            throw new Error(
                data.detail || "Unable to load this document. Please try again."
            );
        }

        return data;
    } catch (error) {
        console.error("Document API Error:", error);

        if (error instanceof TypeError) {
            throw new Error(
                "Unable to connect to the server. Please check your connection and try again."
            );
        }
        throw error;
    }
}

export async function uploadDocument(file) {
    try {
        const token = getAuthToken();
        const formData = new FormData();

        formData.append("file", file);

        const response = await fetch(
            `${API_URL}/documents/upload`,
            {
                method: "POST",
                headers: {
                    Authorization: `Bearer ${token}`
                },
                body: formData
            }
        );

        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
            throw new Error(
                data.detail || "Unable to upload the document. Please try again."
            );
        }

        return data;
    } catch (error) {
        console.error("Upload API Error:", error);

        if (error instanceof TypeError) {
            throw new Error(
                "Unable to connect to the server. Please check your connection and try again."
            );
        }

        throw error;
    }
}

export async function deleteDocument(documentId) {
    try {
        const token = getAuthToken();

        const response = await fetch(
            `${API_URL}/documents/${documentId}`,
            {
                method: "DELETE",
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
            throw new Error(
                data.detail || "Unable to delete the document. Please try again."
            );
        }

        return data;
    } catch (error) {
        console.error("Delete Document API Error:", error);

        if (error instanceof TypeError) {
            throw new Error(
                "Unable to connect to the server. Please check your connection and try again."
            );
        }

        throw error;
    }
}

export async function loginUser(email, password) {
    try {
        const response = await fetch(
            `${API_URL}/login`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email,
                    password
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Login failed."
            );
        }

        return data;

    } catch (error) {
        console.error(
            "Login API Error:",
            error
        );

        throw error;
    }
}

export async function getCurrentUser() {
    try {
        const token = getAuthToken();

        const response = await fetch(
            `${API_URL}/me`,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        if (!response.ok) {
            const errorData = await response.json();

            throw new Error(
                errorData.detail || "Authentication check failed."
            );
        }

        const data = await response.json();

        return data;

    } catch (error) {
        console.error(
            "Current User API Error:",
            error
        );

        throw error;
    }
}

export async function registerUser(email, password) {
    try {
        const response = await fetch(
            `${API_URL}/register`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email,
                    password
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Registration failed."
            );
        }

        return data;

    } catch (error) {
        console.error(
            "Registration API Error:",
            error
        );

        throw error;
    }
}


export async function requestPasswordReset(email) {
    try {
        const response = await fetch(
            `${API_URL}/forgot-password`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Unable to request password recovery."
            );
        }

        return data;
    } catch (error) {
        console.error("Forgot Password API Error:", error);
        throw error;
    }
}


export async function resetPassword(token, newPassword) {
    try {
        const response = await fetch(
            `${API_URL}/reset-password`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    token,
                    new_password: newPassword
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Unable to reset password."
            );
        }

        return data;
    } catch (error) {
        console.error("Reset Password API Error:", error);
        throw error;
    }
}
