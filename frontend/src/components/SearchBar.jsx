import React from 'react';
// 全局SearchBar组件函数
const SearchBar = ({ onSearch, userCampus, searchHistory, token, onClearHistory, onDeleteHistory }) => {
  // 将SearchBar组件导出到全局作用域
  window.SearchBar = SearchBar;
  // 使用React的useState Hook
  const [query, setQuery] = React.useState('');
  // 如果有用户校区设置，则默认选择该校区，否则默认选择全部
  const [location, setLocation] = React.useState(userCampus || ''); // 添加馆藏地筛选状态
  // 添加搜索历史显示/隐藏状态
  const [showHistory, setShowHistory] = React.useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query, location); // 传递查询和馆藏地参数
  }

  // 处理搜索历史点击
  const handleHistoryClick = (historyQuery, historyLocation) => {
    setQuery(historyQuery);
    setLocation(historyLocation);
    onSearch(historyQuery, historyLocation);
  }

  // 处理删除单条搜索历史记录
  const handleDeleteHistory = async (historyId) => {
    if (!token) return;

    try {
      const response = await fetch(`/api/search-history/${historyId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        // 直接更新本地状态，而不是刷新页面
        onDeleteHistory && onDeleteHistory(historyId);
      }
    } catch (error) {
      console.error('删除搜索历史失败:', error);
    }
  }

  // 处理清空所有搜索历史记录
  const handleClearHistory = async () => {
    if (!token) return;

    try {
      const response = await fetch('/api/search-history', {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        // 直接更新本地状态，而不是刷新页面
        onClearHistory && onClearHistory();
      }
    } catch (error) {
      console.error('清空搜索历史失败:', error);
    }
  }

  // 切换搜索历史显示状态
  const toggleHistory = () => {
    setShowHistory(!showHistory);
  }

  // 馆藏地选项
  const locationOptions = [
    { value: '', label: '全部馆藏地' },
    { value: '鼓楼', label: '鼓楼校区' },
    { value: '仙林', label: '仙林校区' },
    { value: '浦口', label: '浦口校区' },
    { value: '苏州', label: '苏州校区' }
  ];

  // 使用React.createElement替代JSX
  return React.createElement('section', { className: 'search-section' },
    React.createElement('form', { className: 'search-form', onSubmit: handleSubmit },
      React.createElement('div', { className: 'search-input-container' },
        React.createElement('div', { className: 'search-input-wrapper' },
          React.createElement('input', {
            type: 'text',
            className: 'search-input',
            placeholder: '请输入书名...',
            value: query,
            onChange: (e) => setQuery(e.target.value),
            autoComplete: 'off'
          }),
          React.createElement('i', { className: 'fas fa-search search-input-icon' })
        ),
        React.createElement('div', { className: 'location-select-wrapper' },
          React.createElement('select', {
            className: 'location-select',
            value: location,
            onChange: (e) => setLocation(e.target.value)
          },
            locationOptions.map(option => React.createElement('option', {
              key: option.value,
              value: option.value
            }, option.label))
          )
        ),
        React.createElement('button', { type: 'submit', className: 'search-button' },
          React.createElement('i', { className: 'fas fa-search mr-2' }),
          '搜索'
        )
      )
    ),
    // 搜索历史显示区域
    React.createElement('div', { className: 'search-history-container' },
      token ? (
        React.createElement('div', null,
          // 搜索历史标题和操作按钮
          React.createElement('div', { className: 'history-header' },
            React.createElement('h3', { className: 'history-title' }, '搜索历史'),
            React.createElement('div', { className: 'history-actions' },
              React.createElement('button', {
                className: 'history-toggle-btn',
                onClick: toggleHistory
              }, showHistory ? '收起' : '展开'),
              React.createElement('button', {
                className: 'history-clear-btn',
                onClick: handleClearHistory,
                disabled: !showHistory || !searchHistory || searchHistory.length === 0
              }, '清空所有')
            )
          ),
          // 搜索历史内容
          showHistory && React.createElement('div', { className: 'search-history' },
            searchHistory && searchHistory.length > 0 ? (
              React.createElement('ul', { className: 'history-list' },
                searchHistory.map((item) => (
                  React.createElement('li', {
                    key: item.id,
                    className: 'history-item'
                  },
                    React.createElement('span', {
                      className: 'history-query',
                      onClick: () => handleHistoryClick(item.query, item.location)
                    }, item.query),
                    item.location && React.createElement('span', {
                      className: 'history-location'
                    }, ` (${item.location})`),
                    React.createElement('button', {
                      className: 'history-delete-btn',
                      onClick: (e) => {
                        e.stopPropagation(); // 防止触发li的点击事件
                        handleDeleteHistory(item.id);
                      }
                    }, '删除')
                  )
                ))
              )
            ) : (
              React.createElement('div', { className: 'history-empty' }, '暂无搜索历史')
            )
          )
        )
      ) : (
        React.createElement('div', { className: 'history-login-prompt' },
          '登录即可查看搜索历史'
        )
      )
    )
  );
}

export default SearchBar;