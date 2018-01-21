import secrets
from sigma.core.mechanics.command import SigmaCommand

import discord

from .mech.interaction_mechanics import grab_interaction, get_target, make_footer


async def dance(cmd: SigmaCommand, message: discord.Message, args: list):
    interaction = await grab_interaction(cmd.db, 'dance')
    target = get_target(message)
    auth = message.author
    icons = ['💃', '🕺']
    icon = secrets.choice(icons)
    if not target or target.id == message.author.id:
        response = discord.Embed(color=0xdd2e44, title=f'{icon} {auth.display_name} dances.')
    else:
        response = discord.Embed(color=0xdd2e44, title=f'{icon} {auth.display_name} dances with {target.display_name}.')
    response.set_image(url=interaction['URL'])
    response.set_footer(text=make_footer(cmd, interaction))
    await message.channel.send(embed=response)
