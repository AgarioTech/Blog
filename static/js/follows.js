async function userFollows(div) {
    const userId = div.getAttribute('data-id')

    const BASE_URL = window.location.origin

    const response = await fetch(`${BASE_URL}/frontend-api/v1/subscription/`, {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
            'user_id': userId
        })
    })
    if (response.status === 401 || response.status === 403) {
        const status = await window.initCheckToken()
        if (status) {
            userFollows(div)
        }
    }

    const data = await response.json()


    if (data.status === 'add') {
        div.style.background = '#E7E8EA'
        div.style.border = '1px solid var(--main-border)'
        div.style.color = '#70737B'
        div.style.fontWeight = '600'
        div.textContent = 'Отписаться'
    } else {
        div.style.background = 'var(--main-color)'
        div.style.color = 'white'
        div.style.border = '1px solid var(--main-color)'
        div.style.fontWeight = ''
        div.textContent = 'Подписаться'
    }
}

async function initUserFollows() {
    const followBtn = document.querySelectorAll('.button-follow')

    const BASE_URL = window.location.origin

    for (const btn of followBtn) {
        const userId = btn.getAttribute('data-id')

        const response = await fetch(`${BASE_URL}/frontend-api/v1/subscription/${userId}/`, {
            method: 'GET',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        if (response.status === 401 || response.status === 403) {
            const status = await window.initCheckToken()
            if (status) {
                initUserFollows()
            }
        }
        const data = await response.json()


        if (response.status === 'subscribed') {
            btn.style.background = '#E7E8EA'
            btn.style.border = '1px solid var(--main-border)'
            btn.style.color = '#70737B'
            btn.style.fontWeight = '600'
            btn.textContent = 'Отписаться'
        } else {
            btn.style.background = 'var(--main-color)'
            btn.style.color = 'white'
            btn.style.border = '1px solid var(--main-color)'
            btn.style.fontWeight = ''
            btn.textContent = 'Подписаться'
        }
    }
}