from app.db import get_connection


conn = get_connection()
cur = conn.cursor()

cur.execute("""
    CREATE TABLE document_chunks (
        id SERIAL PRIMARY KEY,
        document_id INTEGER REFERENCES documents(id),
        chunk_text TEXT,
        embedding vector(384)
    );
""")

conn.commit()

print("document_chunks table created successfully")

cur.close()
conn.close()