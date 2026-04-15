import sqlite3
from datetime import datetime


def create_email_code(
        conn: sqlite3.Connection,
        email: str,
        code: str,
        expire_at: datetime
        ) -> None:
    """新建一条验证码记录"""
    conn.execute(
        """
        INSERT INTO email_codes (email, code, expire_at)
        VALUES (?, ?, ?)
        """,
        (email, code, expire_at.isoformat(),)
    )
    conn.commit()


def get_latest_valid_code(
        conn: sqlite3.Connection,
        email: str
        ) -> sqlite3.Row | None:
    """查找某个邮箱对应的最新的未过期、未使用的验证码记录"""
    cursor = conn.execute(
        """
        SELECT * FROM email_codes
        WHERE email = ? AND used = 0 AND expire_at > CURRENT_TIMESTAMP
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (email,)
    )
    return cursor.fetchone()

def delete_email_code_by_id(
        conn: sqlite3.Connection,
        id: int
        ) -> None:
    """删除一条验证码记录"""
    conn.execute(
        """
        DELETE FROM email_codes WHERE id = ?
        """,
        (id,)
    )
    conn.commit()
def delete_email_codes_by_email(
        conn: sqlite3.Connection,
        email: str
        ) -> None:
    """标记删除某邮箱对应的所有验证码记录"""
    conn.execute(
        """
        DELETE FROM email_codes WHERE email = ?
        """,
        (email,)
    )
    conn.commit()


def mark_code_as_used(
        conn: sqlite3.Connection,
        email: str,
        code: str
        ) -> bool:
    """根据邮箱+验证码标记为已使用，返回是否成功更新"""
    cursor = conn.execute(
        """
        UPDATE email_codes
        SET used = 1
        WHERE email = ? AND code = ? AND used = 0 AND expire_at > CURRENT_TIMESTAMP
        """,
        (email, code,)
    )
    conn.commit()
    return cursor.rowcount > 0
