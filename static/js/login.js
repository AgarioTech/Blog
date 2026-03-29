const logoutButton = document.getElementById('logout')
if (logoutButton) {
    logoutButton.addEventListener('click', async () => {
        const response = await fetch(`${BASE_URL}/users/logout/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': window.csrfToken,
            }
        })
        if (response.ok) {
            window.location.reload()
        }
    })
}
