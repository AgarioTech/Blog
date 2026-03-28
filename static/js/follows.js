async function userFollows(div) {
    const userId = div.getAttribute('data-id')

    const BASE_URL = window.location.origin

    const response = await fetch(`${BASE_URL}/api/v1/users/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
            'user_id': userId
        })
    })
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
    console.log('start follows')
    const followBtn = document.querySelectorAll('.button-follow')

    const BASE_URL = window.location.origin

    for (const btn of followBtn) {
        const userId = btn.getAttribute('data-id')

        const response = await fetch(`${BASE_URL}/api/v1/users/${userId}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        const data = await response.json()


        if (data.status === 'subscribed') {
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