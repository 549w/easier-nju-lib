import streamlit as st
import json
import pandas as pd
from datetime import datetime
from db.connection import get_connection
from repository.usage_log_repo import (
    get_usage_logs,
    get_usage_summary,
    get_daily_stats,
    get_token_cost,
    find_completion_by_prompt
)

# 页面配置
st.set_page_config(
    page_title="Usage Logs Dashboard",
    page_icon="📊",
    layout="wide"
)

# 标题
st.title("LLM Usage Logs Dashboard")

# 获取数据库连接
conn = get_connection()

# 1. 总览指标卡（Dashboard Header）
st.header("📋 Overview")
col1, col2, col3, col4 = st.columns(4)

# 获取使用摘要和token成本
summary = get_usage_summary(conn)
token_cost = get_token_cost(conn)

# 总请求数
with col1:
    st.metric("Total Requests", summary["total_requests"])

# Cache 命中率
with col2:
    cache_hit_rate = summary["cache_hit_rate"] * 100
    st.metric("Cache Hit Rate", f"{cache_hit_rate:.2f}%")
    # 额外优化：用进度条展示 cache hit rate
    st.progress(summary["cache_hit_rate"])

# Token 总消耗
with col3:
    st.metric("Total Tokens", summary["total_tokens"])

# Prompt/Completion Tokens
with col4:
    st.metric("Prompt Tokens", token_cost["prompt_tokens"])
    st.metric("Completion Tokens", token_cost["completion_tokens"])

# 2. 日请求趋势图
st.header("📈 Daily Trends")
daily_stats = get_daily_stats(conn)

if daily_stats:
    # 转换为 DataFrame
    df = pd.DataFrame([{
        "day": row["day"],
        "total_requests": row["total"],
        "cache_hits": row["cache_hits"],
        "tokens": row["tokens"]
    } for row in daily_stats])
    
    # 绘制总请求数和 cache hits
    st.line_chart(df.set_index("day")[["total_requests", "cache_hits"]])
    
    # 绘制 token 使用情况
    st.line_chart(df.set_index("day")["tokens"])
else:
    st.warning("No daily stats available")

# 3. 请求日志列表（核心功能）
st.header("📄 Usage Logs")

# 过滤选项
col1, col2, col3 = st.columns(3)

with col1:
    anon_id_filter = st.text_input("Filter by anon_id")

with col2:
    cache_hit_filter = st.selectbox("Filter by cache hit", ["All", "Yes", "No"])

with col3:
    page_size = st.selectbox("Page size", [20, 50, 100], index=0)

# 分页控制
page = st.session_state.get("page", 1)
if "page" not in st.session_state:
    st.session_state.page = 1

# 计算偏移量
offset = (page - 1) * page_size

# 获取日志数据
try:
    if anon_id_filter:
        logs = get_usage_logs(conn, limit=page_size, offset=offset, anon_id=anon_id_filter)
    else:
        # 注意：get_usage_logs 要求 user_id 或 anon_id 必须提供一个
        # 这里我们需要修改获取所有日志的逻辑
        cursor = conn.execute(
            """
            SELECT * FROM usage_logs
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
            """,
            (page_size, offset,)
        )
        logs = cursor.fetchall()
    
    # 应用 cache_hit 过滤
    if cache_hit_filter != "All":
        is_cache_hit = 1 if cache_hit_filter == "Yes" else 0
        logs = [log for log in logs if log["is_cache_hit"] == is_cache_hit]
    
    # 转换为 DataFrame 用于显示
    log_data = []
    for log in logs:
        total_tokens = (log["prompt_tokens"] or 0) + (log["completion_tokens"] or 0)
        log_data.append({
            "created_at": log["created_at"],
            "anon_id": log["anon_id"],
            "user_id": log["user_id"],
            "ip": log["ip"],
            "user_prompt": log["user_prompt"][:100] + "..." if len(log["user_prompt"]) > 100 else log["user_prompt"],
            "completion_model": log["completion_model"],
            "is_cache_hit": "Yes" if log["is_cache_hit"] else "No",
            "total_tokens": total_tokens
        })
    
    # 显示表格
    if log_data:
        df_logs = pd.DataFrame(log_data)
        st.dataframe(df_logs, use_container_width=True)
        
        # 分页控制
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if page > 1:
                if st.button("Previous Page"):
                    st.session_state.page -= 1
                    st.rerun()
        
        with col2:
            st.write(f"Page {page}")
        
        with col3:
            if len(logs) == page_size:
                if st.button("Next Page"):
                    st.session_state.page += 1
                    st.rerun()
    else:
        st.info("No logs found")
        
    # 4. 单条日志详情展开
    st.subheader("Log Details")
    log_id = st.number_input("Enter log ID to view details", min_value=1, step=1)
    
    if log_id:
        cursor = conn.execute("SELECT * FROM usage_logs WHERE id = ?", (log_id,))
        log = cursor.fetchone()
        
        if log:
            with st.expander(f"Log ID: {log_id}"):
                st.write(f"**Created At:** {log['created_at']}")
                st.write(f"**Anon ID:** {log['anon_id']}")
                st.write(f"**User ID:** {log['user_id']}")
                st.write(f"**IP:** {log['ip']}")
                st.write(f"**Model:** {log['completion_model']}")
                st.write(f"**Is Cache Hit:** {'Yes' if log['is_cache_hit'] else 'No'}")
                st.write(f"**Prompt Tokens:** {log['prompt_tokens']}")
                st.write(f"**Completion Tokens:** {log['completion_tokens']}")
                st.write("\n**User Prompt:**")
                st.code(log['user_prompt'])
                st.write("\n**Completion Content:**")
                try:
                    # 尝试将 completion_content 作为 JSON 美化显示
                    content = json.loads(log['completion_content'])
                    st.json(content)
                except:
                    # 如果不是 JSON，则直接显示
                    st.code(log['completion_content'])
        else:
            st.warning("Log not found")
            
except Exception as e:
    st.error(f"Error fetching logs: {e}")

# 5. Prompt 搜索功能（关键）
st.header("🔍 Prompt Search")
search_prompt = st.text_area("Enter user prompt to search for completion:")

if st.button("Search"):
    if search_prompt:
        completion = find_completion_by_prompt(conn, search_prompt)
        if completion:
            st.success("Cache hit!")
            st.subheader("Completion Content:")
            try:
                # 尝试将 completion 作为 JSON 美化显示
                content = json.loads(completion)
                st.json(content)
            except:
                # 如果不是 JSON，则直接显示
                st.code(completion)
        else:
            st.warning("Cache miss")
    else:
        st.warning("Please enter a prompt to search")

# 额外优化：模糊匹配提示
st.subheader("🔎 Fuzzy Prompt Search")
fuzzy_prompt = st.text_input("Enter partial prompt to search:")

if fuzzy_prompt:
    cursor = conn.execute(
        """
        SELECT user_prompt FROM usage_logs
        WHERE user_prompt LIKE ?
        GROUP BY user_prompt
        LIMIT 10
        """,
        (f"%{fuzzy_prompt}%",)
    )
    suggestions = cursor.fetchall()
    
    if suggestions:
        st.write("Suggestions:")
        for suggestion in suggestions:
            if st.button(suggestion["user_prompt"]):
                # 当用户点击建议时，自动填充到搜索框
                st.session_state.fuzzy_prompt = suggestion["user_prompt"]
                st.rerun()
    else:
        st.info("No suggestions found")

# 关闭数据库连接
conn.close()