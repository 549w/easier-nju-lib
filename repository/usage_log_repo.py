import sqlite3
from datetime import datetime
from typing import List


def create_usage_log(
        conn: sqlite3.Connection,
        user_prompt: str,
        ip: str,
        completion_content: str|None = None,
        prompt_tokens: int|None = None,
        completion_tokens: int|None = None,
        finish_reason: str|None = None,
        completion_id: str|None = None,
        completion_model: str|None = None,
        completed_at: datetime|None = None,
        user_id: int|None = None,
        anon_id: str|None = None,
        is_cache_hit: int = 0,
        ) -> None:
    """创建使用日志记录"""
    if user_id is None and anon_id is None:
        raise ValueError("user_id和anon_id不能同时为空")
    conn.execute(
        """
        INSERT INTO usage_logs (
            user_id, 
            anon_id, 
            ip,
            user_prompt, 
            completion_content,
            prompt_tokens, 
            completion_tokens,
            finish_reason, 
            completion_id, 
            completion_model, 
            completed_at,
            is_cache_hit
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id, 
            anon_id,
            ip, 
            user_prompt, 
            completion_content,
            prompt_tokens, 
            completion_tokens,
            finish_reason, 
            completion_id, 
            completion_model, 
            completed_at.isoformat() if completed_at else None,
            is_cache_hit
        )
    )
    conn.commit()


def get_usage_logs(
        conn: sqlite3.Connection,
        limit: int = 100,
        offset: int = 0,
        user_id: int|None = None,
        anon_id: str|None = None
        ) -> List[sqlite3.Row]:
    """查询指定用户的使用日志，按创建时间倒序排列"""

    if user_id is not None:
        cursor = conn.execute(
            """
            SELECT * FROM usage_logs
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
            """,
            (user_id, limit, offset,)
        )
    elif anon_id is not None:
        cursor = conn.execute(
            """
            SELECT * FROM usage_logs
            WHERE anon_id = ?
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
            """,
            (anon_id, limit, offset,)
        )
    else:
        raise ValueError("user_id和anon_id不能同时为空")
    return cursor.fetchall()


def get_usage_count(
        conn: sqlite3.Connection,
        user_id: int|None = None,
        anon_id: str|None = None
        ) -> int:
    """统计指定用户的使用日志总数"""
    if user_id is not None:
        cursor = conn.execute(
            """
            SELECT COUNT(1) FROM usage_logs
            WHERE user_id = ?
            """,
            (user_id,)
        )
    elif anon_id is not None:
        cursor = conn.execute(
            """
            SELECT COUNT(1) FROM usage_logs
            WHERE anon_id = ?
            """,
            (anon_id,)
        )
    else:
        raise ValueError("user_id和anon_id不能同时为空")
    row = cursor.fetchone()
    return row[0] if row else 0

def find_completion_by_prompt(
        conn: sqlite3.Connection, 
        user_prompt: str
        ) -> str | None:
    cursor = conn.execute(
        """
        SELECT completion_content
        FROM usage_logs
        WHERE user_prompt = ?
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (user_prompt.strip(),)
    )
    row = cursor.fetchone()
    return row[0] if row else None