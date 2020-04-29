const state = {
    isAsideLeftActive: false,
    isBoardActive: false,
    isNotificationsActive: false,
    notification: {
      show: false,
      text: "This is a demo notification"
    }
}

const mutations = {
    setAsideLeftActive (state) {
        state.isAsideLeftActive = !state.isAsideLeftActive
    },
    setBoardActive (state) {
        state.isBoardActive = !state.isBoardActive
    },
    setNotificationsActive (state) {
        state.isNotificationsActive = !state.isNotificationsActive
    }
}

const actions = {
}

export default {
    state,
    mutations,
    actions
}
