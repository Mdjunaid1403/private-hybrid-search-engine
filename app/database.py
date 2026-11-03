import psycopg

from app.db import get_connection
from app.documents import load_documents


def insert_documents(data_folder):
    documents = load_documents(data_folder)

    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            for document in documents:
                cursor.execute(
                    """
                    INSERT INTO documents (filename, content)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING;
                    """,
                    (
                        document["filename"],
                        document["content"]
                    )
                )

        conn.commit()

    finally:
        conn.close()


def get_documents(user_id):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, filename
                FROM documents
                WHERE user_id = %s
                ORDER BY id;
                """,
                (user_id,)
            )

            rows = cursor.fetchall()

            return rows

    finally:
        conn.close()


def get_document(document_id, user_id):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, filename, content
                FROM documents
                WHERE id = %s
                    AND user_id = %s;
                """,
                (document_id, user_id,)
            )

            row = cursor.fetchone()

            return row

    finally:
        conn.close()


def create_user(email, password_hash):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    INSERT INTO users (
                        email,
                        password_hash
                    )
                    VALUES (%s, %s)
                    RETURNING id;
                    """,
                    (
                        email,
                        password_hash
                    )
                )

                row = cursor.fetchone()

            except psycopg.errors.UniqueViolation:
                conn.rollback()
                return "duplicate"

        conn.commit()

        return row[0] if row else None

    finally:
        conn.close()


def get_user_by_email(email):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, email, password_hash
                FROM users
                WHERE email = %s;
                """,
                (email,)
            )

            row = cursor.fetchone()

            return row

    finally:
        conn.close()


def get_user_by_id(user_id):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, email
                FROM users
                WHERE id = %s;
                """,
                (user_id,)
            )

            row = cursor.fetchone()

            return row

    finally:
        conn.close()


def get_documents_for_search(user_id):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, filename, content
                FROM documents
                WHERE user_id = %s
                ORDER BY id;
                """,
                (user_id,)
            )

            rows = cursor.fetchall()

            documents = []

            for row in rows:
                documents.append({
                    "id": row[0],
                    "filename": row[1],
                    "content": row[2]
                })

            return documents

    finally:
        conn.close()


def insert_document(filename, content, user_id):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO documents (filename, content, user_id)
                VALUES (%s, %s, %s)
                ON CONFLICT (user_id, filename) DO NOTHING
                RETURNING id;
                """,
                (filename, content, user_id)
            )

            row = cursor.fetchone()

        conn.commit()

        return row[0] if row else None

    finally:
        conn.close()


def update_document(document_id, filename, content, user_id):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    UPDATE documents
                    SET filename = %s,
                        content = %s
                    WHERE id = %s
                        AND user_id = %s
                    RETURNING id;
                    """,
                    (filename, content, document_id, user_id)
                )

                row = cursor.fetchone()

            except psycopg.errors.UniqueViolation:
                conn.rollback()
                return "duplicate"

        conn.commit()

        return row[0] if row else None

    finally:
        conn.close()


def delete_document(document_id, user_id):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            #First verify that the document belongs to this user
            cursor.execute(
                """
                SELECT id
                FROM documents
                WHERE id = %s
                    AND user_id = %s;
                """, (document_id, user_id)
            )

            document = cursor.fetchone()

            if document is None:
                conn.commit()
                return None

            # Delete chunks and their embeddings first
            cursor.execute("""
                DELETE FROM document_chunks
                WHERE document_id = %s;
            """, (document_id,))

            # Delete the document
            cursor.execute("""
                DELETE FROM documents
                WHERE id = %s
                    AND user_id = %s
                RETURNING id;
            """, (document_id, user_id))

            row = cursor.fetchone()

        conn.commit()

        return row[0] if row else None

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def create_password_reset_table():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS password_reset_tokens (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    token_hash VARCHAR(255) NOT NULL UNIQUE,
                    expires_at TIMESTAMP NOT NULL,
                    used BOOLEAN NOT NULL DEFAULT FALSE,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
            """)

        connection.commit()

    finally:
        connection.close()


def save_password_reset_token(user_id, token_hash, expires_at):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO password_reset_tokens
                    (user_id, token_hash, expires_at)
                VALUES (%s, %s, CURRENT_TIMESTAMP + INTERVAL '15 minutes');
                """,
                (user_id, token_hash)
            )

        connection.commit()

    finally:
        connection.close()


def get_valid_password_reset_token(token_hash):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, user_id
                FROM password_reset_tokens
                WHERE token_hash = %s
                  AND expires_at > CURRENT_TIMESTAMP
                  AND used = FALSE;
                """,
                (token_hash,)
            )

            return cursor.fetchone()

    finally:
        connection.close()


def mark_password_reset_token_used(token_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE password_reset_tokens
                SET used = TRUE
                WHERE id = %s;
                """,
                (token_id,)
            )

        connection.commit()

    finally:
        connection.close()


def update_user_password(user_id, password_hash):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE users
                SET password_hash = %s
                WHERE id = %s;
                """,
                (password_hash, user_id)
            )

        connection.commit()

    finally:
        connection.close()


def reset_user_password_transactionally(token_id, user_id, password_hash):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            # Lock and verify the reset token.
            cursor.execute(
                """
                SELECT id
                FROM password_reset_tokens
                WHERE id = %s
                  AND user_id = %s
                  AND expires_at > CURRENT_TIMESTAMP
                  AND used = FALSE
                FOR UPDATE;
                """,
                (token_id, user_id)
            )

            token_record = cursor.fetchone()

            if token_record is None:
                connection.rollback()
                return False

            # Update the password.
            cursor.execute(
                """
                UPDATE users
                SET password_hash = %s
                WHERE id = %s;
                """,
                (password_hash, user_id)
            )

            if cursor.rowcount != 1:
                connection.rollback()
                return False

            # Mark the token as used.
            cursor.execute(
                """
                UPDATE password_reset_tokens
                SET used = TRUE
                WHERE id = %s
                  AND used = FALSE;
                """,
                (token_id,)
            )

            if cursor.rowcount != 1:
                connection.rollback()
                return False

        connection.commit()
        return True

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
