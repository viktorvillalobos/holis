import Axios from 'axios'

const AxiosDjango = {
  /* eslint-disable-next-line */
  install(Vue, options) {
    if (window.csrf.value) {
      console.log(window.csrf.value)
      Axios.defaults.headers.common['X-CSRF-TOKEN'] = window.csrf.value;
    }

    Vue.$axios = Axios
  }
};

export default AxiosDjango
