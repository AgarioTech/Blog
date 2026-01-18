async function themeFollowFunc(span) {
    const userId = span.getAttribute('data-id')
    const tag = span.getAttribute('datatype')

    const BASE_URL = window.location.origin
    localStorage.setItem('isSearchMode', 'true')

    const request = await fetch(`${BASE_URL}/users/theme-follows/?tag=${tag}`, {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': window.csrfToken,
        },
        body: JSON.stringify({})
        })

    const response = await request.json()

    if (response.status === 'add') {
        span.style.background = '#E7E8EA'
        span.style.color = '#70737B'
        span.style.fontWeight = '600'
        span.textContent = 'Отписаться'
    } else {
        span.style.background = '#4a90e2'
        span.style.color = 'white'
        span.style.fontWeight = ''
        span.textContent = 'Подписаться'
    }
}

async function initThemeFollows() {
    const followBtn = document.querySelector('.theme_subscribe-btn')
    if (followBtn) {
        const tag = followBtn.getAttribute('datatype')
        const userId = followBtn.getAttribute('data-id')

        const BASE_URL = window.location.origin

        if (tag && followBtn && userId && status) {
            const request = await fetch(`${BASE_URL}/users/theme-follows/?tag=${tag}`, {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                }
            })

            if (request.status === 401 || request.status === 403) {
                const status = await window.initCheckToken()
                if (status) {
                    initThemeFollows()
                }
            }

            const response = await request.json()

            if (response.status === 'subscribed') {
                followBtn.style.background = '#E7E8EA'
                followBtn.style.color = '#70737B'
                followBtn.style.fontWeight = '600'
                followBtn.textContent = 'Отписаться'
            } else {
                followBtn.style.background = '#4a90e2'
                followBtn.style.color = 'white'
                followBtn.style.fontWeight = ''
                followBtn.textContent = 'Подписаться'
            }
        }
    }
}