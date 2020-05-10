const state = {
    user: null,
    isAsideLeftActive: false,
    isAsideRightActive: false,
    isBoardActive: true,
    isReleasesActive: false,
    isNotificationsActive: false,
    notification: {
        show: false,
        text: "This is a demo notification"
    },
    isMicroActive: false,
    isSoundActive: true
}

const mutations = {
    setAsideLeftActive(state) {
        state.isAsideLeftActive = !state.isAsideLeftActive
    },
    setAsideRightActive(state) {
        state.isAsideRightActive = !state.isAsideRightActive
    },
    setBoardActive(state) {
        state.isBoardActive = !state.isBoardActive
    },
    setReleasesActive(state) {
        state.isReleasesActive = !state.isReleasesActive
    },
    setNotificationsActive(state) {
        state.isNotificationsActive = !state.isNotificationsActive
    },
    setMicroActive(state) {
        state.isMicroActive = !state.isMicroActive
    },
    setSoundActive(state) {
        state.isSoundActive = !state.isSoundActive
    }
}

const actions = {
}

export default {
    state,
    mutations,
    actions
}
