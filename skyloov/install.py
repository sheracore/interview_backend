from skyloov.users.install import get_users_install


def get_skyloov_app_list_install():
    return list(
        set(get_users_install())
    )
