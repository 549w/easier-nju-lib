// 全局SearchBar组件函数
const SearchBar = ({ onSearch }) => {
  // 使用React的useState Hook
  const [query, setQuery] = React.useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query);
  }

  // 使用React.createElement替代JSX
  return React.createElement('form', { className: 'search-form', onSubmit: handleSubmit },
    React.createElement('div', { className: 'search-input-container' },
      React.createElement('input', {
        type: 'text',
        className: 'search-input',
        placeholder: '请输入书名...',
        value: query,
        onChange: (e) => setQuery(e.target.value),
        autoComplete: 'off'
      }),
      React.createElement('button', { type: 'submit', className: 'search-button' },
        // SVG图标使用简单的文字替代
        '搜索'
      )
    )
  );
}