from app.db import get_connection


conn = get_connection()
cur = conn.cursor()

cur.execute("""
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_name = 'documents'
    ORDER BY ordinal_position;
""")

columns = cur.fetchall()

for column in columns:
    print(column)

cur.close()
conn.close()