async function settings(img) {
    const BASE_URL = window.location.origin
    window.location.href = `${BASE_URL}/settings/`
}

async function profileBookmarksFunc() {
    const bookmarkButton = document.getElementById('profile-nav__item_2')
    const user = bookmarkButton.getAttribute('data-id')
    const BASE_URL = window.location.origin
    profileContentContainer.innerHTML = ''
    nextPostsPageUrl = `${BASE_URL}/frontend-api/v1/posts/get-my-bookmarks-posts/${user}`
    nextCommentsPageUrl = `${BASE_URL}/frontend-api/v1/comments/get-my-bookmarks-comments/${user}`
    isLoadingPosts = false;
    isLoadingComments = false;
    postsContainer = profileContentContainer
    localStorage.setItem('isSearchMode', 'false')
    const isSearchMode = localStorage.getItem('isSearchMode')

    const oldPosts = document.querySelectorAll('.post-wrapper')

    if (oldPosts) {
        oldPosts.forEach(post => post.remove())
    }

    const oldComments = document.querySelectorAll('.comment-item')

    if (oldComments) {
        oldComments.forEach(comment => comment.remove())
    }
    profileContentContainer.innerHTML = ''

    initPostLikes();
    initPostBookmarks();
    initUserFollows();
    initCommentBookmarks();
    initCommentLikes();
}

function profile(username, element=null) {
    window.location.href = `${BASE_URL}/users/${username}/`
    if (element) {
        const profileBookmarks = document.querySelector(`.${element}`)
        profileBookmarks.addEventListener('click', profileBookmarksFunc)
    }
}

function initSettingsPasswordWrapper() {
    const settingsPasswordWrapper = document.querySelector('.settings__password')
    if (settingsPasswordWrapper) {
        settingsPasswordWrapper.style.display = 'none';
    }
};

function showChangeWrapper() {
    const settingsPasswordWrapper = document.querySelector('.settings__password')
    if (settingsPasswordWrapper.style.display === 'none') {
        settingsPasswordWrapper.style.display = 'flex';
    } else { settingsPasswordWrapper.style.display = 'none'; }
}

async function saveProfileData() {
    const usernameError = document.querySelector('.settings__username-error')

    const username = document.querySelector('.settings__username-text').value
    const email = document.querySelector('.settings__email-text').value
    const about = document.querySelector('.settings__about-text').value
    const avatar = document.querySelector('.settings__photo').files[0]

    const data = new FormData()
    data.append('username', username)
    data.append('email', email)
    data.append('about', about)

    if (!avatar) {
        const avatar = document.querySelector('.profile-image').src
        data.append('avatar', avatar)
    } else {
        data.append('avatar', avatar)
    }


    if (username.trim().length < 4) {
        usernameError.textContent = 'Имя пользователя слишком короткое.'
        usernameError.style.color = '#e54848'
    } else {
        const request = await fetch(`${BASE_URL}/users/change-settings-data/`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'X-CSRFToken': window.csrfToken,
            },
            body: data,
        })


        if (request.status === 204) {
            location.reload()
        } else {
            const data = await request.json()
            const dataError = document.querySelector('.settings__errors')
            dataError.textContent = data.error
            dataError.style.color = '#e54848'

            usernameError.textContent = ''
        }
    }
}


async function changePassword(element) {
    const errorElem = document.querySelector('.settings__error-password-message')
    errorElem.textContent = ''

    const username = element.getAttribute('data-key')

    const BASE_URL = window.location.origin

    const oldPassword = document.querySelector('.settings__old-password-text').value
    const newPassword = document.querySelector('.settings__new-password-text').value

    if (!oldPassword || !newPassword) return;

    const request = await fetch(`${BASE_URL}/users/change-settings-password/`, {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
            'old_password':oldPassword,
            'new_password':newPassword,
        })
    })
    const data = await request.json()
    if (request.status === 200) {
        alert('Пароль успешно обновлен')
    } else {
        if (data.error.length) {
            for (let i = 0; i < data.error.length; i++) {
                errorElem.innerHTML += data.error[i] + '<br>'
            }
        } else {
            errorElem.innerHTML += data.error + '<br>'
        }
        errorElem.style.display = 'flex'

    }
}


function adminRedirect() {
    const BASE_URL = window.location.origin
    window.location.href = `${BASE_URL}/admin`
}

function initLoadProfileData() {
    const path = window.location.pathname
    if (path.endsWith('/bookmarks/')) {
        const bookmarkButton = document.getElementById('profile-nav__item_2')
        const profileNavItems = document.querySelectorAll('.profile-nav__item')
        profileNavItems.forEach(el => {
            if (el !== bookmarkButton) {
                el.style.borderBottom = ''

            }
            bookmarkButton.style.borderBottom = '3.5px solid var(--main-color)'
            bookmarkButton.style.color = 'var(--main-color)'
        })
        profileBookmarksFunc()
    }

    if (path.endsWith('/followers/')) {
        const followersButton = document.getElementById('profile-nav__item_4')
        const profileNavItems = document.querySelectorAll('.profile-nav__item')
        profileNavItems.forEach(el => {
            if (el !== followersButton) {
                el.style.borderBottom = ''
            }
            followersButton.style.borderBottom = '3.5px solid var(--main-color)'
            followersButton.style.color = 'var(--main-color)'
        })
        profileFollowersFunc()
    }
    if (path.endsWith('/subscribes/')) {
        const subscribesButton = document.getElementById('profile-nav__item_3')
        const profileNavItems = document.querySelectorAll('.profile-nav__item')
        profileNavItems.forEach(el => {
            if (el !== subscribesButton) {
                el.style.borderBottom = ''
            }
            subscribesButton.style.borderBottom = '3.5px solid var(--main-color)'
            subscribesButton.style.color = 'var(--main-color)'
        })
        profileSubscribesFunc()
    }
    if (path.endsWith(`/${currentProfile}/`)) {
        const postsButton = document.getElementById('profile-nav__item_1')
        const profileNavItems = document.querySelectorAll('.profile-nav__item')
        profileNavItems.forEach(el => {
            if (el !== postsButton) {
                el.style.borderBottom = ''
            }
            postsButton.style.borderBottom = '3.5px solid var(--main-color)'
            postsButton.style.color = 'var(--main-color)'
        })
        profilePostsFunc()
    }
    if (path.endsWith('/comments/')) {
        const commentButton = document.getElementById('profile-nav__item_5')
        const profileNavItems = document.querySelectorAll('.profile-nav__item')

        profileNavItems.forEach(el => {
            if (el !== commentButton) {
                el.style.borderBottom = ''
            }
            commentButton.style.borderBottom = '3.5px solid var(--main-color)'
            commentButton.style.color = 'var(--main-color)'
        })
        profileCommentsFunc()
    }
}

async function profileFollowersFunc() {
    const followersButton = document.getElementById('profile-nav__item_4')
    userId = followersButton.getAttribute('data-auth')
    const followersWrapper = document.createElement('div')
    followersWrapper.classList.add('followers_wrapper')
    followersWrapper.style.display = 'flex'
    isLoadingComments = false;
    isLoadingPosts = true;
    localStorage.setItem('isSearchMode', 'false')

    profileContentContainer.appendChild(followersWrapper)
    profileContentContainer.innerHTML = ''
    followersWrapper.innerHTML = ''

    postsContainer = profileContentContainer

    const oldFollowers = document.querySelectorAll('.follower')

    if (oldFollowers) {
        oldFollowers.forEach(follower => follower.remove())
    }
    profileContentContainer.innerHTML = ''

    const response = await fetch(`${BASE_URL}/frontend-api/v1/subscription/${userId}/get-followers`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    const data = await response.json()
    if (data.followers.length === 0) {
        followersWrapper.style.display = 'none'
    }
    postsContainer = profileContentContainer
    for (let i = 0; i < data.followers.length; i++) {
        const follower = `
            <div class="follower">
                <div class="username-img-wrapper">
                    <img src=${data.followers[i].image} class="following_image">
                    <a class="subs_username" onclick="profile('${data.followers[i].username}')" >${data.followers[i].username}</a>
                </div>
                <div class="button-follow" onclick="userFollows(this)" data-id="${data.followers[i].id}" datatype="${currentUser}">Подписаться</div>
            </div>
        `
        followersWrapper.insertAdjacentHTML('beforeend', follower)
    }
    postsContainer.appendChild(followersWrapper)
    initUserFollows()

}


async function profileSubscribesFunc() {
    const subscribesButton = document.getElementById('profile-nav__item_3')
    userId = subscribesButton.getAttribute('data-auth')
    const followingsWrapper = document.createElement('div')
    followingsWrapper.classList.add('followings_wrapper')
    followingsWrapper.style.display = 'flex'
    isLoadingComments = false;
    isLoadingPosts = true;
    localStorage.setItem('isSearchMode', 'false')

    profileContentContainer.appendChild(followingsWrapper)
    profileContentContainer.innerHTML = ''
    followingsWrapper.innerHTML = ''

    postsContainer = profileContentContainer

    const oldSubscriptions = document.querySelectorAll('.following')

    if (oldSubscriptions) {
        oldSubscriptions.forEach(subscription => subscription.remove())
    }
    profileContentContainer.innerHTML = ''

    const response = await fetch(`${BASE_URL}/frontend-api/v1/subscription/${userId}/get-followers`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    const data = await response.json()
    if (data.followings.length === 0) {
        followingsWrapper.style.display = 'none'
    }
    postsContainer = profileContentContainer
    for (let i = 0; i < data.followings.length; i++) {
        const following = `
            <div class="following">
                <div class="username-img-wrapper">
                    <img src=${data.followings[i].image} class="following_image">
                    <a class="subs_username" onclick="profile('${data.followings[i].username}')" >${data.followings[i].username}</a>
                </div>
                ${currentUser !== data.followings[i].username
                    ?`<div class="button-follow" onclick="userFollows(this)" data-id="${data.followings[i].id}" datatype="${currentUser}">Подписаться</div>`
                    : ``
                }
            </div>
        `
        followingsWrapper.insertAdjacentHTML('beforeend', following)
    }
    postsContainer.appendChild(followingsWrapper)
    initUserFollows()
}

const notificationsWrapper = document.querySelector('.site-header__icon-notifications-wrapper')

notificationsWrapper.addEventListener('click', () => {
    const notificationContainer = document.querySelector('.site-header__notification-container')
    const notificationCount = document.querySelector('.site-header__notifications-count')
    notificationCount.classList.add('hidden')
    localStorage.setItem('isNotificationCountActive', false)
    if (notificationContainer.classList.contains('clicked')) {
        notificationContainer.classList.remove('clicked')
    } else {
        notificationContainer.classList.add('clicked')
    }
})



function profileMenuFunc(element) {
    const profileMenu = document.querySelector('.site-header__account-menu')
    if (profileMenu.classList.contains('clicked')) {
        profileMenu.classList.remove('clicked')
    } else {
        profileMenu.classList.add('clicked')
    }
}

document.addEventListener('click', function (event) {
    const profileMenu = document.querySelector('.site-header__account-menu')
    const profileButton = document.querySelector('.site-header__account-img')
    const notificationButton = document.querySelector('.site-header__icon-notifications-wrapper')
    const notificationContainer = document.querySelector('.site-header__notification-container')

    if (!profileMenu.contains(event.target) && !profileButton.contains(event.target)) {
        profileMenu.classList.remove('clicked')
    }

    if (!notificationButton.contains(event.target) && !notificationContainer.contains(event.target)) {
        notificationContainer.classList.remove('clicked')
    }
})

function initHiddenNotifications() {
    const notificationsState = localStorage.getItem('isNotificationCountActive')
    const notificationCount = document.querySelector('.site-header__notifications-count')
    if (notificationCount) {
        if (notificationsState === 'false') {
            notificationCount.classList.add('hidden')
        } else {
            notificationCount.classList.remove('hidden')
        }
    }

}
