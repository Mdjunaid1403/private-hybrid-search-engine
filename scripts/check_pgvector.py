from app.db import get_connection


conn = get_connection()
cur = conn.cursor()

cur.execute("CREATE EXTENSION vector;")

conn.commit()

print("pgvector extension enabled successfully")

cur.close()
conn.close()