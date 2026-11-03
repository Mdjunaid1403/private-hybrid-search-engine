from app.db import get_connection


conn = get_connection()
cur = conn.cursor()

cur.execute("""
    SELECT column_name, data_type, udt_name
    FROM information_schema.columns
    WHERE table_name = 'document_chunks'
    ORDER BY ordinal_position;
""")

columns = cur.fetchall()

for column in columns:
    print(column)

cur.close()
conn.close()