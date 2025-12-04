// 全局BookCard组件函数
const BookCard = ({ book }) => {
  const { title, author, publisher, year, callNumber, location, status } = book;

  const getStatusColor = (status) => {
    if (status && status.includes('可借')) return 'status-available';
    if (status && status.includes('借出')) return 'status-loaned';
    return 'status-unknown';
  }

  // 使用React.createElement替代JSX
  return React.createElement('div', { className: 'book-card' },
    React.createElement('div', { className: 'book-card-header' },
      React.createElement('h3', { className: 'book-title' }, title || '未知书名'),
      React.createElement('span', { className: `book-status ${getStatusColor(status)}` }, status || '未知状态')
    ),

    React.createElement('div', { className: 'book-card-content' },
      React.createElement('p', { className: 'book-author' }, `作者: ${author || '未知'}`),
      React.createElement('p', { className: 'book-publisher' }, `出版社: ${publisher || '未知'} ${year || ''}`),
      React.createElement('p', { className: 'book-call-number' }, `索书号: ${callNumber || '未知'}`),
      React.createElement('p', { className: 'book-location' }, `馆藏地: ${location || '未知'}`)
    )
  );
}