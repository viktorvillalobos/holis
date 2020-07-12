const BASE_URL = '/api/v1',
    token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
let company;

async function getCompany(val) {
    if (!val) {
        return false
    } else {
        try {
            const { data } = await axios.get(`${BASE_URL}/users/check-company/${val}/`)
            if (data.id) {
                return data
            } else {
                return null
            }
        } catch (e) {
            console.log(e)
            return null
        }
    }
}

function handleBackAndForth(company) {
    const loginForms = document.getElementsByClassName('holis-login-form')
    window.location.href = `${location.protocol}//${company.code}.${location.hostname}:${location.port}/login/`
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
    const company = await getCompany(companyValue)
    btn.classList.toggle('is-loading')

    if (company) {
        handleBackAndForth(company)
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
