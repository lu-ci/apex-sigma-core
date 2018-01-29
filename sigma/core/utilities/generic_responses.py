import discord


def permission_denied(permission: str):
    return discord.Embed(color=0xBE1931, title=f'⛔ Access Denied. You need the {permission} permission.')
