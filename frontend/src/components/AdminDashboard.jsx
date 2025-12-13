import React, { useState, useEffect } from 'react';
import './AdminDashboard.css';

const AdminDashboard = () => {
  const [statistics, setStatistics] = useState(null);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('statistics');

  // 检查用户是否已登录且是管理员
  const checkAdmin = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      setError('请先登录');
      return false;
    }

    try {
      // 检查是否为管理员
      const response = await fetch('/api/admin/statistics', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      return response.ok;
    } catch (err) {
      setError('检查管理员权限失败');
      return false;
    }
  };

  // 获取统计信息
  const fetchStatistics = async () => {
    const token = localStorage.getItem('token');
    if (!token) return;

    try {
      const response = await fetch('/api/admin/statistics', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setStatistics(data.statistics);
      }
    } catch (err) {
      setError('获取统计信息失败');
    }
  };

  // 获取所有用户
  const fetchUsers = async () => {
    const token = localStorage.getItem('token');
    if (!token) return;

    try {
      const response = await fetch('/api/admin/users', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setUsers(data.users);
      }
    } catch (err) {
      setError('获取用户列表失败');
    }
  };

  // 初始化数据
  useEffect(() => {
    const init = async () => {
      const isAdmin = await checkAdmin();
      if (!isAdmin) {
        setError('无管理员权限');
        setLoading(false);
        return;
      }

      // 同时获取统计信息和用户列表
      await Promise.all([
        fetchStatistics(),
        fetchUsers()
      ]);

      setLoading(false);
    };

    init();
  }, []);

  if (loading) {
    return <div className="admin-dashboard">加载中...</div>;
  }

  if (error) {
    return <div className="admin-dashboard">错误: {error}</div>;
  }

  return (
    <div className="admin-dashboard">
      <h1>后台管理面板</h1>

      <div className="admin-tabs">
        <button
          className={activeTab === 'statistics' ? 'active' : ''}
          onClick={() => setActiveTab('statistics')}
        >
          数据看板
        </button>
        <button
          className={activeTab === 'users' ? 'active' : ''}
          onClick={() => setActiveTab('users')}
        >
          用户管理
        </button>
      </div>

      <div className="admin-content">
        {activeTab === 'statistics' && statistics && (
          <div className="statistics-panel">
            <h2>系统统计</h2>
            <div className="statistics-grid">
              <div className="statistic-item">
                <div className="statistic-value">{statistics.user_count}</div>
                <div className="statistic-label">账号总量</div>
              </div>
              <div className="statistic-item">
                <div className="statistic-value">{statistics.access_count}</div>
                <div className="statistic-label">访问总量</div>
              </div>
              <div className="statistic-item">
                <div className="statistic-value">{statistics.search_count}</div>
                <div className="statistic-label">搜索总量</div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'users' && (
          <div className="users-panel">
            <h2>用户列表</h2>
            <table className="users-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>用户名</th>
                  <th>校区</th>
                  <th>创建时间</th>
                </tr>
              </thead>
              <tbody>
                {users.map(user => (
                  <tr key={user.id}>
                    <td>{user.id}</td>
                    <td>{user.username}</td>
                    <td>{user.campus || '-'}</td>
                    <td>{new Date(user.created_at).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;