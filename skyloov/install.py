from skyloov.users.install import get_users_install, get_users_middleware


def get_skyloov_app_list_install():
    return list(
        set(get_users_install())
    )


def get_skyloov_middleware_list():
    return (
        get_users_middleware()
    )