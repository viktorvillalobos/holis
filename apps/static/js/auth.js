const BASE_URL = '/api/v1',
    token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
let company;

async function checkCompany(val) {
    const companyName = document.getElementById('companyName'),
        inputCompany = document.getElementsByName('company')[0];

    if (!val) {
        return false
    } else {
        try {
            const { data } = await axios.get(`${BASE_URL}/users/check-company/${val}`)
            if (data.id) {
                company = data
                companyName.innerText = data.name
                inputCompany.value = data.id
                return true
            } else {
                return false
            }
        } catch (e) {
            return false
        }
    }
}

function handleBackAndForth() {
    const loginForms = document.getElementsByClassName('holis-login-form')
    loginForms[0].classList.toggle('is-active')
    loginForms[1].classList.toggle('is-active')
}

function showHideErrors(error) {
    const toasts = document.getElementsByClassName('js-notifications');
    if (error) {
        for (let i = 0; i < toasts.length; i++) {
            toasts[i].innerHTML = error
            toasts[i].classList.add('is-active')
        }
    } else {
        for (let i = 0; i < toasts.length; i++) {
            toasts[i].classList.remove('is-active')
        }
    }
}

async function handleContinueLogin(e) {
    if (e) e.preventDefault();

    const companyValue = document.getElementsByName('company-check')[0].value,
        btn = document.getElementById('buttonContinue'),
        form = document.getElementById('checkForm');

    if (!companyValue) {
        showHideErrors('You must enter the name of your workspace to continue')
        return
    }
    btn.classList.toggle('is-loading')
    const validate = await checkCompany(companyValue)
    btn.classList.toggle('is-loading')

    if (validate) {
        handleBackAndForth()
        showHideErrors(null)
        form.reset()
    } else {
        showHideErrors('The workspace you are trying to access <strong> still </strong> does not exist.')
        return
    }
}

function handleGoBack() {
    const form = document.getElementById('loginForm')
    form.reset()
    handleBackAndForth()
    showHideErrors(null)
}
