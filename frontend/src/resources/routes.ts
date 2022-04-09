const ACTIVATE_PREFIX = "/activate"

export const routes = {
    root: "/",
    home: "/home",
    download: "/download",
    about: "/about",
    registration: "/registration",
    login: "/login",
    activation: ACTIVATE_PREFIX,
    activateFull: `${ACTIVATE_PREFIX}/:uid/:token`,
};