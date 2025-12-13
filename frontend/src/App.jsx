// 全局App组件函数
import React from 'react';
import SearchBar from './components/SearchBar';
import BookCard from './components/BookCard';
import AdminDashboard from './components/AdminDashboard';
function App() {
  // 将App组件导出到全局作用域
  window.App = App;
  // 使用React的useState Hook
  const [books, setBooks] = React.useState([]);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState(null);
  const [hasSearched, setHasSearched] = React.useState(false);
  // 用户认证状态
  const [user, setUser] = React.useState(null);
  const [token, setToken] = React.useState(localStorage.getItem('token'));
  const [showAuthModal, setShowAuthModal] = React.useState(false);
  const [authMode, setAuthMode] = React.useState('login'); // 'login'或'register'
  // 搜索历史
  const [searchHistory, setSearchHistory] = React.useState([]);
  const [showHistoryModal, setShowHistoryModal] = React.useState(false);
  // 后台管理
  const [showAdminDashboard, setShowAdminDashboard] = React.useState(false);

  // 初始化时获取用户信息和搜索历史
  React.useEffect(() => {
    if (token) {
      fetchUserInfo();
      fetchSearchHistory();
    }
  }, [token]);

  // 获取用户信息
  const fetchUserInfo = async () => {
    try {
      const response = await fetch('/api/user/campus', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        let responseText;
        try {
          responseText = await response.text();

          if (responseText) {
            try {
              const data = JSON.parse(responseText);
              // 从token中提取用户信息（简化处理）
              setUser({ campus: data.campus });
              return;
            } catch (jsonError) {
              console.error('JSON解析错误:', jsonError);
            }
          }
        } catch (textError) {
          console.error('获取响应文本失败:', textError);
        }
      }

      // 如果响应不成功或解析失败，清除token和user
      console.log('获取用户信息失败，清除认证状态');
      localStorage.removeItem('token');
      setToken(null);
      setUser(null);
    } catch (err) {
      console.error('获取用户信息失败:', err);
      // 清除无效的token
      localStorage.removeItem('token');
      setToken(null);
      setUser(null);
    }
  };

  // 获取搜索历史
  const fetchSearchHistory = async () => {
    if (!token) return;
    try {
      const response = await fetch('/api/search-history', { headers: { 'Authorization': `Bearer ${token}` } });

      if (response.ok) {
        let responseText;
        try {
          responseText = await response.text();

          if (responseText) {
            try {
              const data = JSON.parse(responseText);
              // 处理时间格式，确保可以被正确解析
              const processedHistory = data.history.map(item => ({
                ...item,
                // 确保search_time格式正确，兼容不同的时间字符串格式
                search_time: typeof item.search_time === 'string' ? item.search_time : item.search_time.toISOString()
              }));
              setSearchHistory(processedHistory);
              return;
            } catch (jsonError) {
              console.error('JSON解析错误:', jsonError);
            }
          }
        } catch (textError) {
          console.error('获取响应文本失败:', textError);
        }
      }

      console.log('获取搜索历史失败');
    } catch (err) {
      console.error('获取搜索历史失败:', err);
    }
  };

  // 用户注册
  const handleRegister = async (username, password, campus) => {
    try {
      const response = await fetch('/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password, campus })
      });

      let errorMessage = '注册失败';

      // 尝试解析响应内容
      let responseText;
      try {
        responseText = await response.text();

        if (responseText) {
          try {
            const data = JSON.parse(responseText);
            errorMessage = data.error || errorMessage;
          } catch (jsonError) {
            // 不是有效的JSON格式
            errorMessage = `服务器返回错误: ${responseText}`;
          }
        }
      } catch (textError) {
        // 无法获取响应文本
        errorMessage = `网络错误: ${textError.message}`;
      }

      if (!response.ok) {
        throw new Error(errorMessage);
      }

      // 响应成功，解析JSON
      const data = JSON.parse(responseText);
      setToken(data.access_token);
      setUser(data.user);
      localStorage.setItem('token', data.access_token);
      // 获取搜索历史
      fetchSearchHistory();
      setShowAuthModal(false);
      return true;
    } catch (err) {
      alert(err.message);
      return false;
    }
  };

  // 用户登录
  const handleLogin = async (username, password) => {
    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
      });

      let errorMessage = '登录失败';

      // 尝试解析响应内容
      let responseText;
      try {
        responseText = await response.text();

        if (responseText) {
          try {
            const data = JSON.parse(responseText);
            errorMessage = data.error || errorMessage;
          } catch (jsonError) {
            // 不是有效的JSON格式
            errorMessage = `服务器返回错误: ${responseText}`;
          }
        }
      } catch (textError) {
        // 无法获取响应文本
        errorMessage = `网络错误: ${textError.message}`;
      }

      if (!response.ok) {
        throw new Error(errorMessage);
      }

      // 响应成功，解析JSON
      const data = JSON.parse(responseText);
      setToken(data.access_token);
      setUser(data.user);
      localStorage.setItem('token', data.access_token);
      // 获取搜索历史
      fetchSearchHistory();
      setShowAuthModal(false);
      return true;
    } catch (err) {
      alert(err.message);
      return false;
    }
  };

  // 用户登出
  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    setSearchHistory([]);
    setShowAdminDashboard(false);
  };

  // 设置校区
  const handleSetCampus = async (campus) => {
    console.log('handleSetCampus called with:', campus);
    console.log('Current token:', token);
    if (!token) {
      console.log('No token available');
      return;
    }
    try {
      console.log('Sending request to /api/user/campus');
      const response = await fetch('/api/user/campus', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ campus })
      });
      console.log('Response status:', response.status);

      let errorMessage = '校区设置失败';

      // 尝试解析响应内容
      let responseText;
      try {
        responseText = await response.text();

        if (responseText) {
          try {
            const data = JSON.parse(responseText);
            errorMessage = data.error || errorMessage;
          } catch (jsonError) {
            // 不是有效的JSON格式
            errorMessage = `服务器返回错误: ${responseText}`;
          }
        }
      } catch (textError) {
        // 无法获取响应文本
        errorMessage = `网络错误: ${textError.message}`;
      }

      if (response.ok) {
        console.log('Campus update successful, updating local state');
        setUser(prev => ({ ...prev, campus }));
        alert('校区设置成功');
      } else {
        console.log('Campus update failed:', errorMessage);
        alert(errorMessage);
      }
    } catch (err) {
      console.error('设置校区失败:', err);
      alert('设置校区失败: ' + err.message);
    }
  };

  // 搜索功能
  const handleSearch = async (query, location) => {
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setHasSearched(true);

    try {
      if (!token) {
        setError('请先登录');
        setShowAuthModal(true);
        setLoading(false);
        return;
      }

      // 构建URL，添加查询参数
      let url = `/api/search?query=${encodeURIComponent(query)}`;
      if (location) {
        url += `&location=${encodeURIComponent(location)}`;
      }

      // 直接调用后端服务地址，添加认证token
      const response = await fetch(url, { headers: { 'Authorization': `Bearer ${token}` } });

      if (!response.ok) {
        throw new Error('搜索失败');
      }

      let responseText;
      let data = [];

      try {
        responseText = await response.text();

        if (responseText) {
          try {
            data = JSON.parse(responseText);
          } catch (jsonError) {
            console.error('JSON解析错误:', jsonError);
            throw new Error('搜索结果解析失败');
          }
        }
      } catch (textError) {
        console.error('获取响应文本失败:', textError);
        throw new Error('搜索结果获取失败');
      }

      // 直接使用后端返回的图书数组（而不是data.books）
      setBooks(Array.isArray(data) ? data : []);

      // 搜索历史由后端自动记录，不再需要前端单独保存

      // 更新搜索历史
      fetchSearchHistory();
    } catch (err) {
      setError(err.message);
      setBooks([]);
    } finally {
      setLoading(false);
    }
  }

  // 认证模态框组件
  const AuthModal = () => {
    const [username, setUsername] = React.useState('');
    const [password, setPassword] = React.useState('');
    const [campus, setCampus] = React.useState('');

    const handleSubmit = (e) => {
      e.preventDefault();
      if (authMode === 'login') {
        handleLogin(username, password);
      } else {
        // 如果campus为空字符串，则发送null
        handleRegister(username, password, campus || null);
      }
    };

    return React.createElement('div', { className: 'modal-overlay', onClick: () => setShowAuthModal(false) },
      React.createElement('div', { className: 'modal', onClick: (e) => e.stopPropagation() },
        React.createElement('div', { className: 'modal-header' },
          React.createElement('h3', null, authMode === 'login' ? '登录' : '注册'),
          React.createElement('button', { className: 'modal-close', onClick: () => setShowAuthModal(false) }, '×')
        ),
        React.createElement('form', { onSubmit: handleSubmit },
          React.createElement('div', { className: 'form-group' },
            React.createElement('label', { htmlFor: 'username' }, '用户名:'),
            React.createElement('input', {
              type: 'text',
              id: 'username',
              value: username,
              onChange: (e) => setUsername(e.target.value),
              required: true
            })
          ),
          React.createElement('div', { className: 'form-group' },
            React.createElement('label', { htmlFor: 'password' }, '密码:'),
            React.createElement('input', {
              type: 'password',
              id: 'password',
              value: password,
              onChange: (e) => setPassword(e.target.value),
              required: true
            })
          ),
          authMode === 'register' ? React.createElement('div', { className: 'form-group' },
            React.createElement('label', { htmlFor: 'campus' }, '校区:'),
            React.createElement('select', {
              id: 'campus',
              value: campus,
              onChange: (e) => setCampus(e.target.value)
            },
              React.createElement('option', { value: '' }, '请选择校区'),
              React.createElement('option', { value: '鼓楼' }, '鼓楼'),
              React.createElement('option', { value: '仙林' }, '仙林'),
              React.createElement('option', { value: '浦口' }, '浦口'),
              React.createElement('option', { value: '苏州' }, '苏州')
            )
          ) : null,
          React.createElement('div', { className: 'form-actions' },
            React.createElement('button', { type: 'submit', className: 'btn-primary' },
              authMode === 'login' ? '登录' : '注册'
            ),
            React.createElement('button', { type: 'button', className: 'btn-secondary', onClick: () => setAuthMode(authMode === 'login' ? 'register' : 'login') },
              authMode === 'login' ? '没有账号？注册' : '已有账号？登录'
            )
          )
        )
      )
    );
  };

  // 搜索历史模态框组件
  const HistoryModal = () => {
    return React.createElement('div', { className: 'modal-overlay', onClick: () => setShowHistoryModal(false) },
      React.createElement('div', { className: 'modal modal-history', onClick: (e) => e.stopPropagation() },
        React.createElement('div', { className: 'modal-header' },
          React.createElement('h3', null, '搜索历史'),
          React.createElement('button', { className: 'modal-close', onClick: () => setShowHistoryModal(false) }, '×')
        ),
        React.createElement('div', { className: 'modal-body' },
          searchHistory.length === 0 ? React.createElement('p', { className: 'empty-history' }, '暂无搜索历史') :
            React.createElement('div', { className: 'history-list' },
              searchHistory.map((item, index) => React.createElement('div', { key: index, className: 'history-item' },
                React.createElement('div', { className: 'history-query' }, item.query),
                React.createElement('div', { className: 'history-time' }, new Date(item.search_time).toLocaleString()),
                React.createElement('button', {
                  className: 'history-search-btn', onClick: () => {
                    handleSearch(item.query);
                    setShowHistoryModal(false);
                  }
                }, '搜索')
              ))
            )
        )
      )
    );
  };

  // 校区设置组件
  const CampusSetting = () => {
    const campuses = ['鼓楼', '仙林', '浦口', '苏州'];

    return React.createElement('div', { className: 'campus-setting' },
      React.createElement('h4', null, '校区设置'),
      React.createElement('div', { className: 'campus-options' },
        campuses.map(campus => React.createElement('button', {
          key: campus,
          className: `campus-option ${user && user.campus === campus ? 'active' : ''}`,
          onClick: () => handleSetCampus(campus)
        }, campus))
      )
    );
  };

  // 使用React.createElement替代JSX
  return React.createElement('div', { className: 'app' },
    // 顶部导航栏
    React.createElement('header', { className: 'app-header' },
      React.createElement('div', { className: 'header-content' },
        React.createElement('div', { className: 'header-title' },
          React.createElement('h1', null, '南京大学图书馆检索系统'),
          React.createElement('p', null, '快速查找图书馆馆藏图书')
        ),

        // 用户菜单
        React.createElement('div', { className: 'header-user' },
          token && user ? React.createElement('div', { className: 'user-menu' },
            React.createElement('button', { className: 'btn-secondary', onClick: () => setShowHistoryModal(true) }, '搜索历史'),
            // 管理员入口（仅当用户ID为1时显示）
            React.createElement('button', {
              className: 'btn-primary admin-btn',
              onClick: () => setShowAdminDashboard(true)
            }, '后台管理'),
            React.createElement('div', { className: 'user-info' },
              React.createElement('span', null, user.campus ? `校区: ${user.campus}` : '未设置校区'),
              React.createElement('button', { className: 'btn-logout', onClick: handleLogout }, '登出')
            )
          ) : React.createElement('div', { className: 'auth-buttons' },
            React.createElement('button', {
              className: 'btn-primary', onClick: () => {
                setAuthMode('login');
                setShowAuthModal(true);
              }
            }, '登录'),
            React.createElement('button', {
              className: 'btn-secondary', onClick: () => {
                setAuthMode('register');
                setShowAuthModal(true);
              }
            }, '注册')
          )
        )
      )
    ),

    // 校区设置区域
    user ? React.createElement(CampusSetting) : null,

    // 主要内容区
    React.createElement('main', { className: 'app-main' },
      // 传递用户校区信息、搜索历史和token给SearchBar组件
      React.createElement(SearchBar, {
        onSearch: handleSearch,
        userCampus: user?.campus,
        searchHistory: searchHistory,
        token: token,
        onClearHistory: () => setSearchHistory([]),
        onDeleteHistory: (historyId) => setSearchHistory(prev => prev.filter(item => item.id !== historyId))
      }),

      loading ?
        React.createElement('div', { className: 'loading' },
          React.createElement('div', { className: 'loading-spinner' }),
          React.createElement('p', null, '正在搜索中...')
        ) : null,

      error ?
        React.createElement('div', { className: 'error' },
          React.createElement('div', { className: 'error-icon' },
            React.createElement('i', { className: 'fas fa-exclamation-circle' })
          ),
          React.createElement('p', null, error)
        ) : null,

      !loading && !error && hasSearched && books.length === 0 ?
        React.createElement('div', { className: 'empty' },
          React.createElement('div', { className: 'empty-icon' },
            React.createElement('i', { className: 'fas fa-search' })
          ),
          React.createElement('h3', null, '未找到相关图书'),
          React.createElement('p', null, '请尝试使用不同的关键词或调整馆藏地筛选条件')
        ) : null,

      books.length > 0 ?
        React.createElement('div', { className: 'book-grid' },
          books.map((book, index) =>
            React.createElement(BookCard, { key: index, book: book })
          )
        ) : null
    ),



    // 认证模态框
    showAuthModal ? React.createElement(AuthModal) : null,

    // 搜索历史模态框
    showHistoryModal ? React.createElement(HistoryModal) : null,

    // 后台管理面板
    showAdminDashboard ? React.createElement(AdminDashboard) : null
  );
}

export default App;