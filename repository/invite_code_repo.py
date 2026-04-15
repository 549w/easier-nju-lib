import sqlite3
from datetime import datetime


def create_invite_code(
        conn: sqlite3.Connection,
        code_hash: str,
        quota_bonus: int,
        creator_id: int
        ) -> None:
    """新增邀请码"""
    conn.execute(
        """
        INSERT INTO invite_codes (code_hash, quota_bonus, creator_id)
        VALUES (?, ?, ?)
        """,
        (code_hash, quota_bonus, creator_id,)
    )
    conn.commit()

def get_invite_code_by_hash(
        conn: sqlite3.Connection,
        code_hash: str
        ) -> sqlite3.Row | None:
    """根据邀请码哈希值获取邀请码"""
    cursor = conn.execute(
        """
        SELECT * FROM invite_codes
        WHERE code_hash = ?
        """,
        (code_hash,)
    )
    return cursor.fetchone()

def mark_invite_code_as_used(
        conn: sqlite3.Connection,
        code_hash: str,
        user_id: int,
        used_at: datetime
        ) -> bool:
    """标记邀请码为已使用，记录使用时间和使用者ID"""
    cursor = conn.execute(
        """
        UPDATE invite_codes
        SET used = 1, user_id = ?, used_at = ?
        WHERE code_hash = ? AND used = 0
        """,
        (user_id, used_at.isoformat(), code_hash,)
    )
    conn.commit()
    return cursor.rowcount > 0

def delete_invite_code_by_id(
        conn: sqlite3.Connection,
        id: int
        ) -> None:
    """删除邀请码"""
    conn.execute(
        """
        DELETE FROM invite_codes
        WHERE id = ?
        """,
        (id,)
    )
    conn.commit()