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
        setTimeout(() => {
            success.classList.remove('active')
        }, 5000)
        return res;
    } catch (e) {
        btn.classList.remove('is-loading')
        console.error(e);
    }
};

// Navbar menu
function handleNavMenu() {
    console.log('hola')
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
}(document));
