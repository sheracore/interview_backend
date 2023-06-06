from skyloov.users.install import (
    get_users_install,
    get_users_middleware,
)
from skyloov.shops.install import get_shops_install
from skyloov.core.install import get_core_install


def get_skyloov_app_list_install():
    return list(
        set(
            get_users_install()
            + get_shops_install()
            + get_core_install()
            )
    )


def get_skyloov_middleware_list():
    return (
        get_users_middleware()
    )