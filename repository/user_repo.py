import sqlite3

def create_user(
        conn: sqlite3.Connection,
        email: str,
        password_hash: str
        ) -> None:
    conn.execute(
        """
        INSERT INTO users (email, password_hash)
        VALUES (?, ?)
        """,
        (email, password_hash,)
    )
    conn.commit()

def delete_user(
        conn: sqlite3.Connection,
        email: str
        ) -> None:
    conn.execute(
        """
        DELETE FROM users WHERE email = ?
        """,
        (email,)
    )
    conn.commit()

def update_quota(
        conn: sqlite3.Connection,
        email: str,
        quota: int
        ) -> None:
    conn.execute(
        """
        UPDATE users SET quota = ? WHERE email = ?
        """,
        (quota, email,)
    )
    conn.commit()

def get_user_by_email(
        conn: sqlite3.Connection,
        email: str
        ) -> sqlite3.Row | None:
    cursor = conn.execute(
        """
        SELECT * FROM users WHERE email = ?
        """,
        (email,)
    )
    return cursor.fetchone()

def email_exists(
        conn: sqlite3.Connection,
        email: str
        ) -> bool:
    cursor = conn.execute(
        """
        SELECT 1 FROM users WHERE email = ?
        """,
        (email,)
    )
    return cursor.fetchone() is not None