const switchRegisterButton = document.querySelector('.auth-modal__button-switch-to-register')
const switchLoginButton = document.querySelector('.auth-modal__button-switch-to-login')
const registerForm = document.querySelector('.auth-modal-register__wrapper')
const loginForm = document.querySelector('.auth-modal-login__wrapper')

switchRegisterButton.addEventListener('click', () => {
    loginForm.classList.add('auth-modal-login__wrapper--hidden')
    registerForm.classList.remove('auth-modal-register__wrapper--hidden')
})

switchLoginButton.addEventListener('click', () => {
    registerForm.classList.add('auth-modal-register__wrapper--hidden')
    loginForm.classList.remove('auth-modal-login__wrapper--hidden')
})

async function logout() {
    const BASE_URL = window.location.origin

    const request = await fetch(`${BASE_URL}/users/logout/`, {
        method: 'POST',
        credentials: 'include',
        cache: 'reload',
        headers: {
            'X-CSRFToken': window.csrfToken,
        }
    })
    localStorage.clear()
    localStorage.setItem('isLoggingOut', true)
    window.location.href = '/'
}

function initLoginCont() {
    const registerCont = document.querySelector('.register')
    const loginCont = document.querySelector('.login-cont')
    if (registerCont) {
        registerCont.style.display = 'none'
        loginCont.style.display = 'flex'
    }

    localStorage.removeItem('showLogin')
}


