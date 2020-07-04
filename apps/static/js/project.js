/* Project specific Javascript goes here. */

// early access
const BASE_URL = '/api/v1';
const menu = document.getElementsByClassName('espazum-navbar-links')[0]
const token = document.getElementsByName('csrfmiddlewaretoken')[0].value

async function getEarlyAccess(origin) {
    const form = document.getElementById(origin)
    const isValid = form.checkValidity()
    if (!isValid) return

    const input = form.elements[0]
    const email = input.value
    const btn = form.elements[1]
    const success = form.children[1]
    const successSoonAnimation = document.getElementsByClassName('espazum-form-message-animation')
    const successSoonMsg = document.getElementsByClassName('espazum-form-message-msg')

    const config = {
        headers: {
            'X-CSRFToken': token
        }
    }
    const payload = {
        email: email,
        origin: origin
    }

    try {
        btn.classList.add('is-loading')
        const res = await axios.post(`${BASE_URL}/web/get-early-access/`, payload, config);
        btn.classList.remove('is-loading')
        form.reset()
        success.classList.add('active')
        successSoonAnimation[0].classList.toggle('is-active')
        successSoonAnimation[1].classList.toggle('is-active')
        successSoonMsg[0].classList.toggle('is-active')
        successSoonMsg[1].classList.toggle('is-active')
        setTimeout(() => {
            success.classList.remove('active')
            successSoonAnimation[0].classList.toggle('is-active')
            successSoonAnimation[1].classList.toggle('is-active')
            successSoonMsg[0].classList.toggle('is-active')
            successSoonMsg[1].classList.toggle('is-active')
        }, 5000)
        return res;
    } catch (e) {
        btn.classList.remove('is-loading')
        console.error(e);
    }
};

// Navbar menu
function handleNavMenu() {
    menu.classList.toggle('active')
}

!(function (d) {
    // Handle Navbar
    const navbar = d.getElementsByClassName('espazum-navbar')[0]
    window.addEventListener('scroll', function () {
        if (window.scrollY > 80) {
            navbar.classList.add('scrolled')
        } else {
            navbar.classList.remove('scrolled')
        }
    })


    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
}(document));
