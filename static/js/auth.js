async function initCheckToken() {
    const BASE_URL = window.location.origin
    const isLoggingOut = localStorage.getItem('isLoggingOut')
    const response = await fetch(`${BASE_URL}/frontend-api/v1/token/refresh/`, {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    if (response.status === 200) {
        return true
    }
    return false
}
