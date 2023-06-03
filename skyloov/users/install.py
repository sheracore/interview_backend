def get_users_install():
    return ['skyloov', 'skyloov.users']


def get_users_middleware():
    return [
        'skyloov.users.middleware.UserInformationMiddleware',
    ]
