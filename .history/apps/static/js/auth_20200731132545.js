const BASE_URL = '/api/v1',
    token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
let company, inputsCounter = 2;

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
    window.location.href = `${location.protocol}//${location.hostname}:${location.port}/check-company/`
    showHideErrors(null)
}

function stringToSlug(str) {
    str = str.replace(/^\s+|\s+$/g, ''); // trim
    str = str.toLowerCase();

    // remove accents, swap ñ for n, etc
    var from = "àáäâèéëêìíïîòóöôùúüûñç·/_,:;";
    var to = "aaaaeeeeiiiioooouuuunc------";
    for (var i = 0, l = from.length; i < l; i++) {
        str = str.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i));
    }

    str = str.replace(/[^a-z0-9 -]/g, '') // remove invalid chars
        .replace(/\s+/g, '-') // collapse whitespace and replace by -
        .replace(/-+/g, '-'); // collapse dashes

    return str;
}

(function handleCompanyCode() {
    const input = document.getElementById('id_company_name'),
        subdomainField = document.getElementById('subdomain-field'),
        subdomain = document.getElementById('subdomain'),
        companyNameField = document.getElementById('companyNameField')

    subdomainField.style.display = 'none'

    input.addEventListener('input', function (e) {
        suggestCompanyCode(e.srcElement.value, subdomain)

        if (e.srcElement.value && e.srcElement.value !== '') {
            companyNameField.classList.add('is-active')
        } else {
            companyNameField.classList.remove('is-active')
        }
    })
}())

async function suggestCompanyCode(val, setter) {
    try {
        const { data } = await axios.get(`${BASE_URL}/users/suggest-company-code/?company_name=${val}`)
        setter.innerText = stringToSlug(val)
        console.log(data)
    } catch ({ response }) {
        const { data } = response
        setter.innerText = data.recommendations[0]
    }
}

function handleSubdomainChange() {
    const subdomainField = document.getElementById('subdomain-field'),
        companyNameField = document.getElementById('companyNameField');

    if (subdomainField.style.display === 'none') {
        subdomainField.style.display = 'block'
        companyNameField.classList.remove('is-active')
    } else {
        subdomainField.style.display = 'none'
    }
}

function handleInvitationInputs() {
    const inputsWrapper = document.getElementById('inputsWrapper')
    let div = document.createElement('div'),
        input = document.createElement('input'),
        label = document.createElement('label')

    div.classList.add('field')

    label.classList.add('label')
    label.innerText = `Your partner's email`

    input.classList.add('input')
    input.type = 'email'
    input.id = `email${inputsCounter + 1}`
    input.placeholder = 'Ex. juaninjuanharry@mail.com'

    div.appendChild(label)
    div.appendChild(input)
    inputsWrapper.appendChild(div);
    inputsCounter++;
}


function handleFinishInvitations(e) {
    if (e) e.preventDefault();
    const form = document.forms[0],
        input = document.getElementById('id_invitations');

    input.value = ''

    for (let i = 2; i < inputsCounter + 2; i++) {
        if (form[i].value && form[i].value !== '') input.value += `"${form[i].value}",`
    }

    form.submit()
}

function handleFileInput(e) {
    const label = document.getElementById('fileName')
    label.innerText = e[0].name
}

function handlePasswordValidation(val) {
    const passwordField = document.getElementById('passwordField'),
    lettersPill = document.getElementById('pass-letters'),
    numbersPill = document.getElementById('pass-numbers'),
    specialPill = document.getElementById('pass-special');

    if (val) {
        passwordField.classList.add('is-active')
    } else {
        passwordField.classList.remove('is-active')
    }

    if (/[^A-Za-z0-9]/.test(val)) {
        specialPill.style.textDecoration = 'overline'
    } else {
        specialPill.style.textDecoration = ''
    }
    
    if (/[^A-Za-z0-9]/.test(val)) {
        lettersPill.style.textDecoration = 'overline'
    } else {
        lettersPill.style.textDecoration = ''
    }
    
    if (/[^A-Za-z0-9]/.test(val)) {
        lettersPill.style.textDecoration = 'overline'
    } else {
        lettersPill.style.textDecoration = ''
    }
}

function passwordStrength(pw) {
    return /.{8,}/.test(pw) * (  /* at least 8 characters */
        /.{12,}/.test(pw)          /* bonus if longer */
        + /[a-z]/.test(pw)         /* a lower letter */
        + /[A-Z]/.test(pw)         /* a upper letter */
        + /\d/.test(pw)            /* a digit */
        + /[^A-Za-z0-9]/.test(pw)  /* a special character */
    )
}
