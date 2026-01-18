async function sendComment(div) {
    const id = div.getAttribute('data-field-id')
	const comment = document.getElementById(`comment-input-${id}`)
	console.log(id)
	console.log(comment)
	console.log(comment.value)
	const postId = div.getAttribute('data-id')
	console.log(postId)


    const BASE_URL = window.location.origin

    try {
        if (comment.value) {
            const response = await fetch(`${BASE_URL}/frontend-api/v1/comments/`, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({
                    'comment': comment.value,
                    'post': postId,
                })
            })
            if (response.status === 401 || response.status === 403) {
                const status = await window.initCheckToken()
                if (status) {
                    sendComment(div)
                }
            }

            const data = await response.json()
            const description = data.description.replace(
                /@(\w+)/g,
                `<a href="${BASE_URL}/users/$1/" style="color: var(--main-color);">@$1</a>`
            )

            const newComment = `
                <div class="comment-item" id="comment-item-${data.id}">
                    <div class="comment-item__user-info">
                        <img src="${data.image}" class="comment-item__user-icon">
                        ${currentUser == data.username
                        ? `
                            <div class="comment-item__user-info-details">
                                <a href="${BASE_URL}/${data.username}" style="color: white; font-weight: 500; font-size: 13px;">${data.username}</a>
                            </div>`
                        : `${data.username}`}
                        <span class="comment-item__pub-date">${smart_time(data.pub_date)}</span>
                    </div>
                    <div class="comment-item__content">
                        ${description}
                    </div>
                    <div class="comment-reactions">
                        <div class="comment__like-button" onclick="setCommentLike(this)" data-id="${data.id}" data-type="common">
                            <img src="/media/icons/hart.png" class="comment__like-icon">
                            <span class="comment__likes-count" id="comment__likes-count-id-${data.id}">${data.likes}</span>
                        </div>
                        <div class="comment__bookmark-button" onclick="setCommentBookmark(this)" data-id="${data.id}" data-section="bookmarks">
                            <a>
                                <svg class="comment__bookmark-icon" width="24" height="24" viewBox="0 0 24 24">
                                    <path d="M6 2C5.44772 2 5 2.44772 5 3V21C5 21.2761 5.22386 21.5 5.5 21.5C5.63261 21.5 5.76522 21.4477 5.85355 21.3536L12 15.7071L18.1464 21.3536C18.2348 21.4477 18.3674 21.5 18.5 21.5C18.7761 21.5 19 21.2761 19 21V3C19 2.44772 18.5523 2 18 2H6Z" stroke-width="2"/>
                                </svg>
                            </a>
                            <span class="comment__bookmark-count" id="comment__bookmark-count-id-${data.id}">${data.bookmarked_by.length}</span>
                        </div>
                        <span class="comment__reply-button" onclick="commentReply(this)" data-field-id="${postID}" data-id="${data.id}" datatype="commentReplyButton">Ответить</span>
                        ${currentUser == data.username ? `
                        <span class="comment__delete-button" onclick="commentDelete(this)" id="${data.id}" data-key="${data.id}" data-type="common" data-id="${data.post_id}">Удалить</span>
                    ` : ''}
                    </div>
                    <div class="send_comment__form" id="send_comment__form-${data.id}">
                        <textarea id="comment-input-${data.id}" class="comment-input" placeholder="Комментарий" id="reply_comment-input-${data.id}"></textarea>
                        <div class="send-comment__button" id="comment-${data.id}" onclick="sendComment(this)" data-field-id="${data.id}" data-key="${data.id}" data-id="${data.post_id}">Отправить</div>
                    </div>
                </div>
            `

            const commentsCont = document.querySelector('.comments-list')
            commentsCont.insertAdjacentHTML('beforeend', newComment)
        }
    } catch (error) {
        console.log(error)
    }

}

async function initLoadComments() {
    if (!nextCommentsPageUrl || isLoadingComments) return;
    isLoadingComments = true

    const response = await fetch(nextCommentsPageUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    if (response.status === 401 || response.status === 403) {
        const status = await window.initCheckToken()
        if (status) {
            initLoadComments()
        }
    }
    const data = await response.json()
    nextCommentsPageUrl = data.pages.next

    for (let i = 0; i < data.results.length; i++) {
        const newComment = `
            <div class="profile__comment-wrapper" id="comment-item-${data.results[i].id}">
                <a href="/post/${data.results[i].post_id}" class="post__title">${data.results[i].post}</a>
                <div class="comment-item" id="comment-item-${data.results[i].id}">
                    <div class="comment-item__user-info">
                        <img src="${data.results[i].image}" class="comment-item__user-icon">
                        ${currentUser == data.results[i].username
                        ? `
                            <div class="comment-item__user-info-details">
                                <a href="${BASE_URL}/${data.results[i].username}" style="color: white; font-weight: 500; font-size: 13px;">${data.results[i].username}</a>
                            </div>`
                        : `${data.results[i].username}`}
                        <span class="comment-item__pub-date">${smart_time(data.results[i].pub_date)}</span>
                    </div>
                    <div class="comment-item__content">
                        ${data.results[i].description}
                    </div>
                    <div class="comment-reactions">
                        <div class="comment__like-button" onclick="setCommentLike(this)" data-id="${data.results[i].id}" data-type="common">
                            <img src="/media/icons/hart.png" class="comment__like-icon">
                            <span class="comment__likes-count" id="comment__likes-count-id-${data.results[i].id}">${data.results[i].likes}</span>
                        </div>
                        <div class="comment__bookmark-button" onclick="setCommentBookmark(this)" data-id="${data.results[i].id}" data-section="bookmarks">
                            <a>
                                <svg class="comment__bookmark-icon" width="24" height="24" viewBox="0 0 24 24">
                                    <path d="M6 2C5.44772 2 5 2.44772 5 3V21C5 21.2761 5.22386 21.5 5.5 21.5C5.63261 21.5 5.76522 21.4477 5.85355 21.3536L12 15.7071L18.1464 21.3536C18.2348 21.4477 18.3674 21.5 18.5 21.5C18.7761 21.5 19 21.2761 19 21V3C19 2.44772 18.5523 2 18 2H6Z" stroke-width="2"/>
                                </svg>
                            </a>
                            <span class="comment__bookmark-count" id="comment__bookmark-count-id-${data.results[i].id}">${data.results[i].bookmarked_by.length}</span>
                        </div>
                        <span class="comment__reply-button" onclick="commentReply(this)" data-field-id="${postID}" data-id="${data.results[i].id}" datatype="commentReplyButton">Ответить</span>
                        ${currentUser == data.results[i].username ? `
                        <span class="comment__delete-button" onclick="commentDelete(this)" id="${data.results[i].id}" data-key="${data.results[i].id}" data-type="common" data-id="${data.results[i].post_id}">Удалить</span>
                    ` : ''}
                    </div>
                    <div class="send_comment__form" id="send_comment__form-${data.results[i].id}">
                        <textarea id="comment-input-${data.results[i].id}" class="comment-input" placeholder="Комментарий" id="reply_comment-input-${data.results[i].id}"></textarea>
                        <div class="send-comment__button" id="comment-${data.results[i].id}" onclick="sendComment(this)" data-field-id="${data.results[i].post_id}" data-key="${data.results[i].id}" data-id="${data.results[i].id}">Отправить</div>
                    </div>
                </div>
            </div>
        `
        postsContainer.insertAdjacentHTML('beforeend', newComment)

    }
    initCommentLikes()
    initCommentBookmarks()
    initCommentLikes()
    initUserFollows();
    isLoadingComments = false
}


async function initLoadPostComments() {
    if (!nextCommentsPageUrl || isLoadingComments) return;
    const moreComments = localStorage.getItem('moreComments')
    iSsLoadingComments = true

    const response = await fetch(nextCommentsPageUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    const data = await response.json()
    nextCommentsPageUrl = data.pages.next

    for (let i = 0; i < data.results.length; i++) {
        const description = data.results[i].description.replace(
            /@(\w+)/g,
            `<a href="${BASE_URL}/users/$1/" style="color: var(--main-color);">@$1</a>`
        )
        const newComment = `
            <div class="comment-item" id="comment-item-${data.results[i].id}">
                <div class="comment-item__user-info">
                    <img src="${data.results[i].image}" class="comment-item__user-icon">
                    ${currentUser == data.results[i].username
                    ? `
                        <div class="comment-item__user-info-details">
                            <a href="${BASE_URL}/${data.results[i].username}" style="color: white; font-weight: 500; font-size: 13px;">${data.results[i].username}</a>
                        </div>`
                    : `${data.results[i].username}`}
                    <span class="comment-item__pub-date">${smart_time(data.results[i].pub_date)}</span>
                </div>
                <div class="comment-item__content">
                    ${description}
                </div>
                <div class="comment-reactions">
                    <div class="comment__like-button" onclick="setCommentLike(this)" data-id="${data.results[i].id}" data-type="common">
                        <img src="/media/icons/hart.png" class="comment__like-icon">
                        <span class="comment__likes-count" id="comment__likes-count-id-${data.results[i].id}">${data.results[i].likes}</span>
                    </div>
                    <div class="comment__bookmark-button" onclick="setCommentBookmark(this)" data-id="${data.results[i].id}" data-section="bookmarks">
                        <a>
                            <svg class="comment__bookmark-icon" width="24" height="24" viewBox="0 0 24 24">
                                <path d="M6 2C5.44772 2 5 2.44772 5 3V21C5 21.2761 5.22386 21.5 5.5 21.5C5.63261 21.5 5.76522 21.4477 5.85355 21.3536L12 15.7071L18.1464 21.3536C18.2348 21.4477 18.3674 21.5 18.5 21.5C18.7761 21.5 19 21.2761 19 21V3C19 2.44772 18.5523 2 18 2H6Z" stroke-width="2"/>
                            </svg>
                        </a>
                        <span class="comment__bookmark-count" id="comment__bookmark-count-id-${data.results[i].id}">${data.results[i].bookmarked_by.length}</span>
                    </div>
                    <span class="comment__reply-button" onclick="commentReply(this)" data-field-id="${postID}" data-id="${data.results[i].id}" datatype="commentReplyButton">Ответить</span>
                    ${currentUser == data.results[i].username ? `
                    <span class="comment__delete-button" onclick="commentDelete(this)" id="${data.results[i].id}" data-key="${data.results[i].id}" data-type="common" data-id="${data.results[i].post_id}">Удалить</span>
                ` : ''}
                </div>
                <div class="send_comment__form" id="send_comment__form-${data.results[i].id}">
                    <textarea id="comment-input-${data.results[i].id}" class="comment-input" placeholder="Комментарий" id="reply_comment-input-${data.results[i].id}"></textarea>
                    <div class="send-comment__button" id="comment-${data.results[i].id}" onclick="sendComment(this)" data-field-id="${data.results[i].id}" data-key="${data.results[i].id}" data-id="${data.results[i].post_id}">Отправить</div>
                </div>
            </div>
        `
        commentsContainer.insertAdjacentHTML('beforeend', newComment)

    }

    if (data.count - data.results.length > 0 && moreComments === 'false') {
        moreCommentsButton = `<div class="hidden-comments__button" onclick="moreCommentsFunc()" >
                                        <span>Показать ${data.count - data.results.length} ${smart_word_end(data.count - data.results.length)}</span>
                                    </div>`
        postDetailContainer.insertAdjacentHTML('beforeend', moreCommentsButton)
    }

    initCommentLikes()
    initCommentBookmarks()
    initCommentLikes()
    initUserFollows();
    isLoadingComments = false



}

function moreCommentsFunc() {
    localStorage.setItem('moreComments', true)
    moreCommentsClass = document.querySelector('.hidden-comments__button')
    moreCommentsClass.style.display = 'none'

}


async function profileCommentsFunc() {
    const commentButton = document.getElementById('profile-nav__item_5')
    const user = commentButton.getAttribute('data-id')
    const BASE_URL = window.location.origin
    const currentUser = commentButton.getAttribute('data-auth')

    profileContentContainer.innerHTML = ''

    nextCommentsPageUrl = `${BASE_URL}/frontend-api/v1/comments/get-user-comments/${user}`
    isLoadingComments = false;
    isLoadingPosts = true;
    localStorage.setItem('isSearchMode', 'false')
    postsContainer = profileContentContainer

    const oldComments = document.querySelectorAll('.comment-item')

    if (oldComments) {
        oldComments.forEach(comment => comment.remove())
    }
    profileContentContainer.innerHTML = ''

    initLoadComments()
}

function initLoadCommentForm() {
    document.querySelectorAll(`.send_comment__form`).forEach(el => {
        if (el.id === `send_comment__form-${postID}`) {
            el.style.display = 'flex'
        }
    })
}

async function commentReply(span) {
    const replyCount = span.getAttribute('datatype')
    let textContent_1 = 'Ответить'
    let textContent_2 = 'Отмена'
    const postId = span.getAttribute('data-field-id')
    const commentId = span.getAttribute('data-id')
    let commentWrapper = ''
    document.querySelectorAll(`.send_comment__form`).forEach(el => {
        if (el.id === `send_comment__form-${commentId}`) {
            el.style.display = 'flex'
            commentWrapper = el

        } else {
            el.style.display = 'none'
            span.textContent = textContent_1
        }

    })


    if (span.classList.contains('deployed')) {
        document.querySelectorAll(`.send_comment__form`).forEach(el => {
            if (el.id === `send_comment__form-${postId}`) {
                el.style.display = 'flex'
            } else {
                el.style.display = 'none'
            }
        })

        commentWrapper.style.display = 'none'
        span.textContent = textContent_1
        span.classList.add('hidden')
        span.classList.remove('deployed')

    } else {
        document.querySelectorAll(`span[datatype="${span.getAttribute('datatype')}"]`).forEach(el => {
            if (el.textContent === textContent_2) {
                el.textContent = textContent_1
            }
        })

        span.classList.add('deployed')
        span.textContent = textContent_2
        span.classList.add('hidden')
        commentWrapper.style.display = 'flex'
    }
}



async function commentDelete(span) {
    const type = span.getAttribute('data-type')
    const postId = span.getAttribute('data-id')
    const id = span.getAttribute('data-key')
    let commentsCont = document.querySelector('.comments-list')
    const BASE_URL = window.location.origin

    const response = await fetch(`${BASE_URL}/frontend-api/v1/comments/${id}/`, {
        method: 'DELETE',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': window.csrfToken,
        }
    })
    if (response.status === 401 || response.status === 403) {
        const status = await window.initCheckToken()
        if (status) {
            commentDelete(span)
        }
    }
    if (!commentsCont) {
        commentsCont = document.querySelector('.profile-header-nav-cont')
    }
    if (request.status === 204) {
        const successMessage = document.createElement('div')
        successMessage.innerText = 'Комментарий удален'
        successMessage.style.color = 'var(--main-color)'
        const delComment = document.getElementById(`comment-item-${id}`)
        commentsCont.replaceChild(successMessage, delComment)
    }
}


async function setCommentLike(div) {
	const id = div.getAttribute("data-id");
	let likesCount = ''
	const commentType = div.getAttribute("data-type")

    likesCount = document.getElementById(`comment__likes-count-id-${id}`);


	const BASE_URL = window.location.origin


	try {
        const response = await fetch(`${BASE_URL}/frontend-api/v1/comments/${id}/set-like/`, {
            method: 'GET',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        if (response.status === 401 || response.status === 403) {
            const status = await window.initCheckToken()
            if (status) {
                setCommentLike(div)
            }
        }

        const data = await response.json()

        likesCount.textContent = data.likes;

        if (data.liked) {
            div.classList.add("comment__like-button--active")
            likesCount.classList.remove('setlikeanimate', 'dellikeanimate')
            void likesCount.offsetWidth
            likesCount.classList.add('dellikeanimate');
        } else {
            div.classList.remove("comment__like-button--active")
            likesCount.classList.remove('setlikeanimate', 'dellikeanimate')
            void likesCount.offsetWidth
            likesCount.classList.add('setlikeanimate');
        }

	} catch (error) {
        console.log(error);
    }
}


async function initCommentLikes() {

    const imgWrapper = document.querySelectorAll(".comment__like-button");
    const BASE_URL = window.location.origin

    for (const img of imgWrapper) {
        const id = img.getAttribute("data-id");
        const likesCount = document.getElementById(`comment__likes-count-id-${id}`);

        try {
            const response = await fetch(`${BASE_URL}/frontend-api/v1/comments/${id}`, {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            if (response.status === 401 || response.status === 403) {
                const status = await window.initCheckToken()
                if (status) {
                    initCommentLikes()
                }
            }
            const data = await response.json();

            if (data.is_authenticated) {
                if (data.liked) {
                    img.classList.add("comment__like-button--active")
                    likesCount.classList.remove('setlikeanimate', 'dellikeanimate'); // Убираем все
                    void likesCount.offsetWidth; // Принудительная перерисовка
                    likesCount.classList.add('dellikeanimate');
                } else {
                    img.classList.remove("comment__like-button--active")
                    likesCount.classList.remove('setlikeanimate', 'dellikeanimate'); // Убираем все
                    void likesCount.offsetWidth; // Принудительная перерисовка
                    likesCount.classList.add('setlikeanimate');
                }
            } else {
                img.classList.remove("comment__like-button--active")
                likesCount.classList.remove('setlikeanimate', 'dellikeanimate'); // Убираем все
                void likesCount.offsetWidth; // Принудительная перерисовка
                likesCount.classList.add('setlikeanimate');
            }
        } catch (error) {
            console.error(error);
        }
    }
}