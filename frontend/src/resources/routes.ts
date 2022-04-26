const ACTIVATE_PREFIX = "/activate"
const PASSWORD_RESET_PREFIX = "/password-reset"

export const routes = {
    root: "/",
    home: "/home",
    download: "/download",
    about: "/about",
    registration: "/registration",
    registrationCompleted: "/registration-completed",
    login: "/login",
    activation: `${ACTIVATE_PREFIX}`,
    activateFull: `${ACTIVATE_PREFIX}/:uid/:token`,
    passwordReset: `${PASSWORD_RESET_PREFIX}`,
    passwordResetFull: `${PASSWORD_RESET_PREFIX}/:uid/:token`,
};