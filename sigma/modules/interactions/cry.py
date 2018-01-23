import discord

from .mech.interaction_mechanics import grab_interaction, get_target, make_footer


async def cry(cmd, message, args):
    interaction = await grab_interaction(cmd.db, 'cry')
    target = get_target(message)
    auth = message.author
    if not target or target.id == message.author.id:
        response = discord.Embed(color=0x5dadec, title=f'😢 {auth.display_name} cries.')
    else:
        response = discord.Embed(color=0x5dadec,
                                 title=f'😢 {auth.display_name} cries because of {target.display_name}.')
    response.set_image(url=interaction['URL'])
    response.set_footer(text=make_footer(cmd, interaction))
    await message.channel.send(embed=response)
