ROLE_NAMES = ('Administrador', 'Professor', 'Estudante')


def get_user_role(user):
    if not user.is_authenticated:
        return 'Visitante'

    group_names = {group.name for group in user.groups.all()}
    for role in ROLE_NAMES:
        if role in group_names:
            return role
    if user.is_superuser:
        return 'Administrador'
    return 'Estudante'