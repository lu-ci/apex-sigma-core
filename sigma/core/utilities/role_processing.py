def mat_rl(role_name, server=None, user=None):
    match = None
    generator = None
    if server:
        generator = server.roles
    elif user:
        generator = user.roles
    for role in generator:
        if role.name.lower() == role_name.lower():
            match = role
    return match


def matching_role(server, role_name):
    return mat_rl(role_name, server=server)


def user_matching_role(user, role_name):
    return mat_rl(role_name, user=user)
