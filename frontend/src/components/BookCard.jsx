// 全局BookCard组件函数
import React from 'react';

const BookCard = ({ book }) => {
  const { title, author, publisher, year, holdings } = book;

  // 获取状态颜色的辅助函数
  const getStatusColor = (status) => {
    if (status && status.includes('可借')) return 'status-available';
    if (status && status.includes('借出')) return 'status-loaned';
    return 'status-unknown';
  }

  // 处理馆藏信息 - 兼容两种格式：直接字段和holdings数组
  let holdingsToDisplay = [];

  // 检查是否有直接字段（兼容旧格式）
  if (book.callNumber) {
    holdingsToDisplay.push({
      callNumber: book.callNumber || '未知',
      location: book.location || '未知',
      status: book.status || '未知状态'
    });
  } else if (holdings && holdings.length > 0) {
    // 如果有holdings数组，使用所有馆藏信息
    holdingsToDisplay = holdings.map(holding => ({
      callNumber: holding.callNumber || '未知',
      location: holding.location || '未知',
      status: holding.status || '未知状态'
    }));
  } else {
    // 默认馆藏信息
    holdingsToDisplay.push({
      callNumber: '未知',
      location: '未知',
      status: '未知状态'
    });
  }
  // 使用React.createElement替代JSX
  return React.createElement('div', { className: 'book-card' },
    React.createElement('div', { className: 'book-card-header' },
      React.createElement('h3', { className: 'book-title' }, title || '未知书名')
    ),

    React.createElement('div', { className: 'book-card-content' },
      React.createElement('p', { className: 'book-author' }, `作者: ${author || '未知'}`),
      React.createElement('p', { className: 'book-publisher' }, `出版社: ${publisher || '未知'} ${year || ''}`),

      // 显示所有馆藏信息
      React.createElement('div', { className: 'book-holdings' },
        holdingsToDisplay.map((holding, index) =>
          React.createElement('div', { key: index, className: 'holding-item' },
            React.createElement('span', { className: `book-status ${getStatusColor(holding.status)}` }, holding.status),
            React.createElement('span', { className: 'book-call-number' }, `索书号: ${holding.callNumber}`),
            React.createElement('span', { className: 'book-location' }, `馆藏地: ${holding.location}`)
          )
        )
      )
    )
  );
}

export default BookCard;