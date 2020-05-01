const state = {
    isAsideLeftActive: false,
    isAsideRightActive: true,
    isBoardActive: false,
    isNotificationsActive: false,
    notification: {
        show: false,
        text: "This is a demo notification"
    },
    isMicroActive: true,
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
