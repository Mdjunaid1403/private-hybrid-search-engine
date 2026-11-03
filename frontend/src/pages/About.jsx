function About() {
    return (
        <div className="about-section">
            <h1>About Private Search</h1>

            <p>
                Private Search is a privacy-focused hybrid search engine
                designed to search private local documents and the web.
            </p>

            <h2>Search Capabilities</h2>

            <ul>
                <li>Keyword Search</li>
                <li>Semantic Search</li>
                <li>Hybrid Search</li>
                <li>Web Search</li>
            </ul>

            <h2>Technology Stack</h2>

            <ul>
                <li>Frontend: React + TypeScript</li>
                <li>Backend: Python + FastAPI</li>
                <li>Database: PostgreSQL + pgvector</li>
                <li>Embeddings: Sentence Transformers</li>
                <li>Web Search: DuckDuckGo</li>
            </ul>
        </div>
    );
}

export default About;