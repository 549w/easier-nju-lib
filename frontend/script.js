const { createApp, ref, reactive, computed } = Vue

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
        const currentCardIndex = ref(0) // 当前卡片索引

        // 拖拽相关变量
        const isDragging = ref(false)
        const startX = ref(0)
        const startY = ref(0)
        const currentX = ref(0)
        const currentY = ref(0)
        const cardRotation = ref(0)

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
                '可借': { class: 'bg-success/20 text-success', icon: 'check' },
                '在架': { class: 'bg-success/20 text-success', icon: 'newsstand' },
                '签收': { class: 'bg-success/20 text-success', icon: 'inventory' },
                '借出': { class: 'bg-warning/20 text-warning', icon: 'block' },
                '委托借出': { class: 'bg-warning/20 text-warning', icon: 'handshake' },
                '阅览': { class: 'bg-primary/20 text-primary', icon: 'import_contacts' },
                '装订中': { class: 'bg-primary/20 text-primary', icon: 'attach_file' },
                '交接': { class: 'bg-primary/20 text-primary', icon: 'transform' },
                '上委托书架': { class: 'bg-warning/20 text-warning', icon: 'shelves' },
                '下架': { class: 'bg-danger/20 text-danger', icon: 'do_not_disturb_on' },
                '正常': { class: 'bg-success/10 text-success', icon: 'auto_awesome' },
                '编目中': { class: 'bg-primary/10 text-primary', icon: 'edit_note' }
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

            const errorMap = {
                TOO_LONG: "请精简表达，不多于五十个字。"
            };

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
                    throw {
                        "code": errorData.detail?.code || "UNKNOWN_ERROR",
                        "message": errorData.detail?.message || "有点南搜"
                    }
                }

                const data = await response.json();
                currentQuery.value = data.query; // 保存查询体用于翻页
                total.value = data.result.total;

                // 初始化书籍状态
                books.value = data.result.books.map(b => ({
                    ...b,
                    _isFlipped: false,
                    _loadingItems: false,
                    _itemsLoaded: false,
                    _items: [],
                    _itemsTotal: 0
                }));

                // 重置卡片索引
                currentCardIndex.value = 0;


            } catch (error) {
                console.error(error);
                errorMessage.value = errorMap[error.code] || "有点南搜……";
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
                    _isFlipped: false,
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

        // 计算卡片宽度和间隙
        const cardWidth = Math.min(window.innerWidth * 0.9, 420); // 响应式卡片宽度
        const gap = 24; // 卡片之间的间隙
        const containerWidth = window.innerWidth; // 容器宽度

        // 计算轨道样式
        const trackStyle = computed(() => {
            const baseOffset = -currentCardIndex.value * (cardWidth + gap);

            // 居中补偿（关键）
            const centerOffset = (containerWidth - cardWidth) / 2;

            const dragOffset = isDragging.value ? currentX.value : 0;

            return {
                width: `${books.value.length * (cardWidth + gap)}px`,
                transform: `translateX(${baseOffset + centerOffset + dragOffset}px)`,
                transition: isDragging.value ? 'none' : 'transform 380ms cubic-bezier(0.22, 1, 0.36, 1)',
                touchAction: 'pan-y'
            }
        })

        // 开始拖拽
        const startDrag = (event) => {
            isDragging.value = true

            // 记录起始位置
            if (event.type === 'mousedown') {
                startX.value = event.clientX
                startY.value = event.clientY
            } else if (event.type === 'touchstart') {
                startX.value = event.touches[0].clientX
                startY.value = event.touches[0].clientY
            }

            currentX.value = 0
            currentY.value = 0
        }

        // 拖拽中
        const onDrag = (event) => {
            if (!isDragging.value) return

            // 计算拖拽距离
            let clientX, clientY
            if (event.type === 'mousemove') {
                clientX = event.clientX
                clientY = event.clientY
            } else if (event.type === 'touchmove') {
                clientX = event.touches[0].clientX
                clientY = event.touches[0].clientY
            }

            currentX.value = clientX - startX.value
            currentY.value = clientY - startY.value

            // 限制滑动方向：如果垂直滑动更明显，不触发横向滑动
            if (Math.abs(currentY.value) > Math.abs(currentX.value)) {
                return
            }

            // 只允许水平拖拽，阻止垂直滚动
            if (Math.abs(currentX.value) > Math.abs(currentY.value)) {
                event.preventDefault()
            }
        }

        // 结束拖拽
        const endDrag = () => {
            if (!isDragging.value) return

            isDragging.value = false

            // 计算拖拽阈值
            const threshold = window.innerWidth * 0.2

            // 判断是否达到阈值
            if (currentX.value > threshold) {
                // 向右滑动，切换到上一张卡片
                currentCardIndex.value = Math.max(0, currentCardIndex.value - 1)
            } else if (currentX.value < -threshold) {
                // 向左滑动，切换到下一张卡片
                currentCardIndex.value = Math.min(books.value.length - 1, currentCardIndex.value + 1)

                // 当滑动到倒数第三张卡片时，自动加载更多
                if (currentCardIndex.value >= books.value.length - 3 && books.value.length < total.value) {
                    loadMore()
                }
            }

            // 重置拖拽状态
            currentX.value = 0
            currentY.value = 0
            cardRotation.value = 0
        }

        // 阻止事件冒泡
        const stopPropagation = (event) => {
            event.stopPropagation()
        }

        // 卡片翻面功能
        const toggleFlip = async (book) => {
            // 翻转卡片
            book._isFlipped = !book._isFlipped

            // 如果翻转到反面且未加载馆藏信息，加载馆藏信息
            if (book._isFlipped && !book._itemsLoaded) {
                book._loadingItems = true

                try {
                    const response = await fetch(`/search/items/${book.book_id}?page=1&rows=100`)
                    if (!response.ok) throw new Error('获取馆藏详情失败')

                    const data = await response.json()
                    let fetchedItems = data.items || []

                    // 如果有校区限制，则进行排序：符合校区的排在前面
                    if (currentQuery.value && currentQuery.value.campusId) {
                        const restrictedCampuses = currentQuery.value.campusId.filter(id => id !== null)
                        if (restrictedCampuses.length > 0) {
                            fetchedItems.sort((a, b) => {
                                const aMatch = restrictedCampuses.includes(a.campus_id) ? 1 : 0
                                const bMatch = restrictedCampuses.includes(b.campus_id) ? 1 : 0
                                return bMatch - aMatch
                            })
                        }
                    }

                    book._items = fetchedItems
                    book._itemsTotal = data.total || 0
                    book._itemsLoaded = true
                } catch (error) {
                    console.error('获取馆藏失败:', error)
                    errorMessage.value = `书籍《${book.title}》的馆藏信息加载失败`
                } finally {
                    book._loadingItems = false
                }
            }
        }

        // 预加载机制
        const preloadBooks = () => {
            // 预加载下一本书的封面
            if (currentCardIndex.value + 1 < books.value.length) {
                const nextBook = books.value[currentCardIndex.value + 1]
                if (nextBook && nextBook.cover) {
                    const img = new Image()
                    img.src = nextBook.cover
                }
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
            currentCardIndex,
            charCount,
            canSearch,
            getStatusStyle,
            isPreferredCampus,
            searchBooksNL,
            loadMore,
            toggleFlip,
            trackStyle,
            startDrag,
            onDrag,
            endDrag,
            stopPropagation
        }
    }
}).mount('#app')