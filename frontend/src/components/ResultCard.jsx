function ResultCard({
    filename,
    keywordScore,
    semanticScore,
    hybridScore
}) {
    return (
        <div className="result-card">
            <div className="result-header">
                <h3>{filename}</h3>

                <span className="result-score">
                    Hybrid score: {hybridScore.toFixed(3)}
                </span>
            </div>

            <p className="result-preview">
                Keyword score: {keywordScore.toFixed(3)}
                {" | "}
                Semantic score: {semanticScore.toFixed(3)}
            </p>
        </div>
    );
}

export default ResultCard;