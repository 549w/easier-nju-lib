const { createApp, ref, reactive } = Vue

createApp({
    setup() {
        const intentPhrase = ref('')
        const isSearching = ref(false)
        const isLoadingMore = ref(false)
        const searched = ref(false)
        const errorMessage = ref('')

        const books = ref([])
        const total = ref(0)
        const currentQuery = ref(null) // 存储从 /nl 返回的结构化 query

        // 计算输入字符数
        const charCount = Vue.computed(() => {
            return intentPhrase.value.length
        })

        // 判断是否可以搜索（非空且不超过50字）
        const canSearch = Vue.computed(() => {
            return intentPhrase.value.trim() && charCount.value <= 50
        })

        // 状态颜色和图标映射
        const getStatusStyle = (statusName) => {
            const styles = {
                '可借': { class: 'bg-green-100 text-green-800', icon: 'check' },
                '在架': { class: 'bg-green-100 text-green-800', icon: 'newsstand' },
                '签收': { class: 'bg-green-100 text-green-800', icon: 'inventory' },
                '借出': { class: 'bg-orange-100 text-orange-800', icon: 'block' },
                '委托借出': { class: 'bg-orange-100 text-orange-800', icon: 'handshake' },
                '阅览': { class: 'bg-blue-100 text-blue-800', icon: 'import_contacts' },
                '装订中': { class: 'bg-blue-100 text-blue-800', icon: 'attach_file' },
                '交接': { class: 'bg-blue-100 text-blue-800', icon: 'transform' },
                '上委托书架': { class: 'bg-yellow-100 text-yellow-800', icon: 'shelves' },
                '下架': { class: 'bg-red-100 text-red-800', icon: 'do_not_disturb_on' },
                '正常': { class: 'bg-green-50 text-green-700', icon: 'auto_awesome' },
                '编目中': { class: 'bg-blue-50 text-blue-700', icon: 'edit_note' }
            };
            return styles[statusName] || { class: 'bg-gray-100 text-gray-800', icon: 'info' };
        }

        // 判断是否是用户要求的校区
        const isPreferredCampus = (campusId) => {
            if (!currentQuery.value || !currentQuery.value.campusId) return false;
            // 过滤掉 null 的情况
            const restrictedCampuses = currentQuery.value.campusId.filter(id => id !== null);
            if (restrictedCampuses.length === 0) return false;
            return restrictedCampuses.includes(campusId);
        }

        // 发起首次自然语言搜索
        const searchBooksNL = async () => {
            if (!intentPhrase.value.trim() || isSearching.value) return;

            isSearching.value = true;
            searched.value = false;
            errorMessage.value = '';
            books.value = [];
            total.value = 0;
            currentQuery.value = null;

            try {
                const response = await fetch('/search/books/llm_query', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        intent_phrase: intentPhrase.value,
                        page: 1,
                        rows: 10
                    })
                });

                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({ detail: '网络请求失败' }));
                    throw new Error(errorData.detail || '搜索请求失败，请稍后重试');
                }

                const data = await response.json();
                currentQuery.value = data.query; // 保存查询体用于翻页
                total.value = data.result.total;

                // 初始化书籍状态
                books.value = data.result.books.map(b => ({
                    ...b,
                    _showItems: false,
                    _loadingItems: false,
                    _itemsLoaded: false,
                    _items: [],
                    _itemsTotal: 0
                }));
            } catch (error) {
                console.error(error);
                errorMessage.value = "无法理解你的搜索意图💔";
            } finally {
                isSearching.value = false;
                searched.value = true;
            }
        }

        // 加载更多（翻页）
        const loadMore = async () => {
            if (!currentQuery.value || isLoadingMore.value) return;

            isLoadingMore.value = true;
            errorMessage.value = '';

            try {
                // 复制 query 并页码 +1
                const nextQuery = { ...currentQuery.value };
                nextQuery.page += 1;

                const response = await fetch('/search/books/normal_query', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(nextQuery)
                });

                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({ detail: '加载更多失败' }));
                    throw new Error(errorData.detail || '无法加载更多内容');
                }

                const data = await response.json();

                // 更新当前的 query 为最新页码
                currentQuery.value = nextQuery;

                // 追加书籍并初始化状态
                const newBooks = data.books.map(b => ({
                    ...b,
                    _showItems: false,
                    _loadingItems: false,
                    _itemsLoaded: false,
                    _items: [],
                    _itemsTotal: 0
                }));

                books.value = [...books.value, ...newBooks];
            } catch (error) {
                console.error('加载更多出错:', error);
                errorMessage.value = error.message;
            } finally {
                isLoadingMore.value = false;
            }
        }

        // 切换展示馆藏信息
        const toggleBookItems = async (book) => {
            // 如果已经展开，则收起
            if (book._showItems) {
                book._showItems = false;
                return;
            }

            // 展开
            book._showItems = true;
            errorMessage.value = '';

            // 如果已经加载过，直接返回
            if (book._itemsLoaded) return;

            // 开始加载
            book._loadingItems = true;

            try {
                const response = await fetch(`/search/items/${book.book_id}?page=1&rows=100`); // 默认拉取前100条馆藏
                if (!response.ok) throw new Error('获取馆藏详情失败');

                const data = await response.json();
                let fetchedItems = data.items || [];

                // 如果有校区限制，则进行排序：符合校区的排在前面
                if (currentQuery.value && currentQuery.value.campusId) {
                    const restrictedCampuses = currentQuery.value.campusId.filter(id => id !== null);
                    if (restrictedCampuses.length > 0) {
                        fetchedItems.sort((a, b) => {
                            const aMatch = restrictedCampuses.includes(a.campus_id) ? 1 : 0;
                            const bMatch = restrictedCampuses.includes(b.campus_id) ? 1 : 0;
                            return bMatch - aMatch; // 1 (匹配) 排在 0 (不匹配) 前面
                        });
                    }
                }

                book._items = fetchedItems;
                book._itemsTotal = data.total || 0;
                book._itemsLoaded = true;
            } catch (error) {
                console.error('获取馆藏失败:', error);
                errorMessage.value = `书籍《${book.title}》的馆藏信息加载失败`;
            } finally {
                book._loadingItems = false;
            }
        }

        return {
            intentPhrase,
            isSearching,
            isLoadingMore,
            searched,
            errorMessage,
            books,
            total,
            charCount,
            canSearch,
            getStatusStyle,
            isPreferredCampus,
            searchBooksNL,
            loadMore,
            toggleBookItems
        }
    }
}).mount('#app')