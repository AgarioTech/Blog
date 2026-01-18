

async function searchPosts() {
    const BASE_URL = window.location.origin
    const query = document.querySelector('.site-header__input-search').value
    localStorage.setItem('isSearchMode', 'true')

    if (lastQuery !== query) {
        const params = new URLSearchParams(window.location.search)
        params.set('query', query)
        nextPostsPageUrl = `${BASE_URL}/frontend-api/v1/search/?${params.toString()}`
        lastQuery = query

        const oldPosts = document.querySelectorAll('.post-wrapper')

        if (oldPosts) {
            oldPosts.forEach(post => post.remove())
        }
    }

    isLoading = false

    if (!nextPostsPageUrl || isLoadingPosts) return;
    isLoadingPosts = true

    const response = await fetch(nextPostsPageUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    const data = await response.json()
    nextPostsPageUrl = data.pages.next

    const postsContainer = document.querySelector('.posts-container')

    const oldPosts = document.querySelectorAll('.post')

    if (oldPosts) {
        oldPosts.forEach(post => post.remove())
    }

    const badImg = document.querySelector('.bad-search-img')
    if (data.results.length === 0) {
        badImg.style.display = 'flex'
    } else {
        badImg.style.display = 'none'
        for (let i = 0; i < data.results.length; i++) {
            if (document.getElementById(`post-${data.results[i].id}`)) continue;
                const posts = `
                    <div class="post" id="post-${data.results[i].id}">
                        <div class="post__header">
                            <div class="user-info">
                                <div class="user-info__meta">
                                    <img src="${data.results[i].image}" class="user-info__avatar">
                                        <div class="user-info__details">
                                            <a href="${window.BASE_URL}/users/${data.results[i].user}" class="user-info__username">${data.results[i].user}</a>
                                            <div class="user-info__date">${smart_time(data.results[i].pub_date)}</div>
                                        </div>
                                    </div>
                                    ${currentUser !== data.results[i].user
                                        ? `<div class="button-follow" onclick="userFollows(this)" data-id="${data.results[i].user_id}" datatype="${currentUser}">Подписаться</div>`
                                        : ''
                                    }
                                </div>
                            <br>
                                <div class="post__meta">
                                    <a href="${BASE_URL}/${data.results[i].tag}" class="post__category">${data.results[i].category}</a>
                                    <div class="post__type">${data.results[i].post_type}</div>
                                </div>
                            <br>
                            <br>
                            <div class="post__title">
                                <a href="/post/${data.results[i].id}">${data.results[i].title}</a>
                            </div>
                            <br>
                            <div class="post__content">
                                ${data.results[i].wrapp_img
                                    ? `<img src="${data.results[i].wrapp_img}" class="post__wrapp-img">`
                                    : ''
                                }
                                <p>${splitContent(data.results[i].content)}</p>
                            </div>
                            <div class="post__button-detail">
                                <a href="/post/${data.results[i].id}/">Читать далее</a>
                            </div>
                            <div class="post__actions">
                                <div class="reactions">
                                    <div class="like-button" onclick="setPostLike(this)" data-id="${data.results[i].id}">
                                        <img src="/media/icons/hart.png" class="like-button__icon">
                                        <span class="like-button__count" id="like-button__count-id-${data.results[i].id}">${data.results[i].liked_by.length}</span>
                                    </div>
                                    <div class="comment-button">
                                        <img src="/media/icons/comment.svg" class="comment-button__icon" onclick="window.location.href = '/post/${data.results[i].id}/'">
                                        <span class="comment-button__count">${data.results[i].comment_count}</span>
                                    </div>
                                    <div class="bookmark-button" onclick="setPostBookmark(this)" data-id="${data.results[i].id}" data-section="bookmarks">
                                        <svg class="bookmark-button__icon" width="24" height="24" viewBox="0 0 24 24">
                                            <path d="M6 2C5.44772 2 5 2.44772 5 3V21C5 21.2761 5.22386 21.5 5.5 21.5C5.63261 21.5 5.76522 21.4477 5.85355 21.3536L12 15.7071L18.1464 21.3536C18.2348 21.4477 18.3674 21.5 18.5 21.5C18.7761 21.5 19 21.2761 19 21V3C19 2.44772 18.5523 2 18 2H6Z" stroke-width="2"/>
                                        </svg>
                                        <span class="bookmark-button__count" id="bookmark-button__count-id-${data.results[i].id}">${data.results[i].bookmark_user.length}</span>
                                    </div>
                                </div>
                                <div class="post__views">
                                    <img src="/media/icons/view.svg" class="post__view-icon">
                                    <span class="post__view-count">${data.results[i].views_count}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                `
            postsContainer.insertAdjacentHTML('beforeend', posts)
        }
    }
    initPostBookmarks()
    initPostLikes()
    initUserFollows()
    isLoadingPosts = false
    localStorage.setItem('isSearchMode', true)
}








