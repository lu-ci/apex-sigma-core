import arrow
import discord

from sigma.core.utilities.data_processing import get_time_difference, user_avatar


async def leave_logger(ev, member):
    response = discord.Embed(color=0xBE1931, timestamp=arrow.utcnow().datetime)
    response.set_author(name=f'A Member Has Left', icon_url=user_avatar(member))
    response.add_field(name='📤 Leaving Member', value=f'{member.mention}\n{member.name}#{member.discriminator}')
    new_acc, diff_msg = get_time_difference(member, leave=True)
    response.add_field(name='🕑 Member Joined', value=f'{diff_msg.title()}', inline=True)
    response.set_footer(text=f'UserID: {member.id}')
    await log_event(ev.db, member.guild, response)
