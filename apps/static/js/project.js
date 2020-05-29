/* Project specific Javascript goes here. */

const BASE_URL = '/api/v1/';
async function getEarlyAccess(origin) {
    const form = document.getElementById(origin)
    const input = form.elements[0]
    const email = input.value
    const btn = form.elements[1]
    const success = form.children[1]
    const payload = {
        email: email,
        origin: origin
    }

    try {
        btn.classList.add('is-loading')
        const res = await axios.post(`${BASE_URL}/web/get-early-access/`, payload);
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
    // Get early access form
}(document));