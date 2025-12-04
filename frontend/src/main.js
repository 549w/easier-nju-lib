// 使用CDN版本的React
const { createRoot } = ReactDOM;

// 创建根节点并渲染应用
const root = createRoot(document.getElementById('root'));

// 使用React.StrictMode渲染App组件
root.render(
  React.createElement(React.StrictMode, null,
    React.createElement(App)
  )
);