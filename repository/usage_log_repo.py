import sqlite3
from datetime import datetime
from typing import List


def create_usage_log(
        conn: sqlite3.Connection,
        user_id: int,
        user_prompt: str,
        prompt_tokens: int,
        completion_tokens: int,
        finish_reason: str,
        completion_id: str,
        completion_model: str,
        completed_at: datetime
        ) -> None:
    """创建使用日志记录"""
    conn.execute(
        """
        INSERT INTO usage_logs (
            user_id, user_prompt, prompt_tokens, completion_tokens,
            finish_reason, completion_id, completion_model, completed_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id, user_prompt, prompt_tokens, completion_tokens,
            finish_reason, completion_id, completion_model, completed_at.isoformat()
        )
    )
    conn.commit()


def get_usage_logs_by_user(
        conn: sqlite3.Connection,
        user_id: int,
        limit: int = 100,
        offset: int = 0
        ) -> List[sqlite3.Row]:
    """查询指定用户的使用日志，按创建时间倒序排列"""
    cursor = conn.execute(
        """
        SELECT * FROM usage_logs
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
        """,
        (user_id, limit, offset,)
    )
    return cursor.fetchall()


def get_usage_count_by_user(
        conn: sqlite3.Connection,
        user_id: int
        ) -> int:
    """统计指定用户的使用日志总数"""
    cursor = conn.execute(
        """
        SELECT COUNT(1) FROM usage_logs
        WHERE user_id = ?
        """,
        (user_id,)
    )
    row = cursor.fetchone()
    return row[0] if row else 0
