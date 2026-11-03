from app.db import get_connection


conn = get_connection()
cur = conn.cursor()

cur.execute("""
    SELECT atttypmod
    FROM pg_attribute
    WHERE attrelid = 'document_chunks'::regclass
    AND attname = 'embedding';
""")

result = cur.fetchone()

print("Vector dimension:", result[0])

cur.close()
conn.close()