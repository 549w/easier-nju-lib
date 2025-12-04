from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# 设置Chrome选项
chrome_options = Options()
chrome_options.add_argument('--headless')  # 无头模式
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920x1080')
chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

# 创建WebDriver实例
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

try:
    # 访问南京大学图书馆OPAC系统搜索页面
    search_url = 'https://opac.nju.edu.cn/opac/openlink.php'
    search_params = {
        'strSearchType': 'title',
        'match_flag': 'forward',
        'strText': 'Python',
        'doctype': 'ALL',
        'page': 1
    }
    
    # 构建完整的URL
    import urllib.parse
    full_url = f"{search_url}?{urllib.parse.urlencode(search_params)}"
    
    print(f"访问URL: {full_url}")
    driver.get(full_url)
    
    # 等待页面加载
    time.sleep(5)
    
    # 打印页面标题
    print(f"页面标题: {driver.title}")
    
    # 打印页面源代码长度
    print(f"页面源代码长度: {len(driver.page_source)}")
    
    # 保存页面源代码到文件
    with open('opac_page.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    print("页面源代码已保存到 opac_page.html")
    
    # 尝试获取网络请求（需要更高级的selenium配置）
    # 这里我们尝试直接从页面中提取可能的数据
    print("\n尝试从页面中提取数据...")
    
    # 查找所有script标签
    scripts = driver.find_elements(By.TAG_NAME, 'script')
    print(f"找到 {len(scripts)} 个script标签")
    
    # 检查每个script标签，寻找可能包含数据的
    for i, script in enumerate(scripts):
        script_content = script.get_attribute('innerHTML')
        if script_content.strip():
            # 查找可能的数据结构
            if 'window.' in script_content or 'var ' in script_content or 'const ' in script_content:
                print(f"\nScript {i+1} 包含变量定义")
                # 保存到文件以便分析
                with open(f'script_{i+1}.js', 'w', encoding='utf-8') as f:
                    f.write(script_content)
                print(f"Script {i+1} 已保存到 script_{i+1}.js")
                    
    # 检查是否有iframe
    iframes = driver.find_elements(By.TAG_NAME, 'iframe')
    print(f"找到 {len(iframes)} 个iframe")
    
    # 检查页面中的主要元素
    app_element = driver.find_element(By.ID, 'app')
    print(f"找到app元素: {app_element.tag_name}")
    
finally:
    # 关闭浏览器
    driver.quit()
    print("\n浏览器已关闭")