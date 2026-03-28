const switchRegisterButton = document.querySelector('.auth-modal__button-switch-to-register')
const switchLoginButton = document.querySelector('.auth-modal__button-switch-to-login')
const registerForm = document.querySelector('.auth-modal-register__wrapper')
const loginForm = document.querySelector('.auth-modal-login__wrapper')
const logoutButton = document.querySelector('.logout')


if (switchRegisterButton) {
   switchRegisterButton.addEventListener('click', () => {
       loginForm.classList.add('auth-modal-login__wrapper--hidden')
       registerForm.classList.remove('auth-modal-register__wrapper--hidden')
    })
}

if (switchLoginButton) {
    switchLoginButton.addEventListener('click', () => {
        registerForm.classList.add('auth-modal-register__wrapper--hidden')
        loginForm.classList.remove('auth-modal-login__wrapper--hidden')
    })
}


function initLoginCont() {
    const registerCont = document.querySelector('.register')
    const loginCont = document.querySelector('.login-cont')
    if (registerCont) {
        registerCont.style.display = 'none'
        loginCont.style.display = 'flex'
    }

}

if (logoutButton) {
    logoutButton.addEventListener('click', async () => {
        console.log('logged out')
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


