import arrow
import discord

from sigma.core.utilities.data_processing import user_avatar


async def userinformation(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    response = discord.Embed(color=target.color)
    response.set_author(name=f'{target.display_name}\'s Information', icon_url=user_avatar(target))
    creation_time = arrow.get(target.created_at).format('DD. MMMM YYYY')
    user_text = f'Username: **{target.name}**#{target.discriminator}'
    user_text += f'\nID: **{target.id}**'
    user_text += f'\nStatus: **{str(target.status).replace("dnd", "busy").title()}**'
    user_text += f'\nBot User: **{target.bot}**'
    user_text += f'\nCreated: **{creation_time}**'
    response.add_field(name='User Info', value=user_text, inline=True)
    member_join_time = arrow.get(target.joined_at).format('DD. MMMM YYYY')
    is_moderator = target.permissions_in(message.channel).manage_guild
    member_text = f'Name: **{target.display_name}**'
    member_text += f'\nColor: **{str(target.color).upper()}**'
    member_text += f'\nTop Role: **{target.top_role.name}**'
    member_text += f'\nModerator: **{is_moderator}**'
    member_text += f'\nJoined: **{member_join_time}**'
    response.add_field(name='Member Info', value=member_text, inline=True)
    pfx = await cmd.bot.get_prefix(message)
    footer = f'To see the user\'s avatar use the {pfx}avatar command.'
    response.set_footer(text=footer)
    await message.channel.send(None, embed=response)
