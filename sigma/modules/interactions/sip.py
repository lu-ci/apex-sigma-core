import discord
from sigma.core.mechanics.command import SigmaCommand

from .mech.interaction_mechanics import grab_interaction, get_target, make_footer


async def sip(cmd: SigmaCommand, message: discord.Message, args: list):
    interaction = await grab_interaction(cmd.db, 'sip')
    target = get_target(message)
    auth = message.author
    if not target or target.id == message.author.id:
        response = discord.Embed(color=0xa6d388, title=f'🍵 {auth.display_name} sips their beverage.')
    else:
        response = discord.Embed(color=0xa6d388,
                                 title=f'🍵 {auth.display_name} takes a sip with {target.display_name}.')
    response.set_image(url=interaction['URL'])
    response.set_footer(text=make_footer(cmd, interaction))
    await message.channel.send(embed=response)
