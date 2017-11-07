import discord


def mat_rl(role_name, server=None, user=None):
    if server:
        generator = server.roles
    elif user:
        generator = user.roles
    else:
        generator = None
    if generator:
        match = discord.utils.find(lambda x: x.name.lower() == role_name.lower(), generator)
    else:
        match = None
    return match


def matching_role(server, role_name):
    return mat_rl(role_name, server=server)


def user_matching_role(user, role_name):
    return mat_rl(role_name, user=user)
