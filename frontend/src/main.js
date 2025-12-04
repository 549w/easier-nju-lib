// 使用CDN版本的React
const { createRoot } = ReactDOM;

// 创建根节点并渲染应用
const [您的服务器用户名] = createRoot(document.getElementById('[您的服务器用户名]'));

// 使用React.StrictMode渲染App组件
[您的服务器用户名].render(
  React.createElement(React.StrictMode, null,
    React.createElement(App)
  )
);