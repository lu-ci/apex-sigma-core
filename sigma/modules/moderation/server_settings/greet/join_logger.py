import arrow
import discord

from sigma.core.utilities.data_processing import get_time_difference, user_avatar


async def join_logger(ev, member):
    response = discord.Embed(color=0x66CC66, timestamp=arrow.utcnow().datetime)
    response.set_author(name=f'A Member Has Joined', icon_url=user_avatar(member))
    response.add_field(name='📥 Joining Member', value=f'{member.mention}\n{member.name}#{member.discriminator}')
    new_acc, diff_msg = get_time_difference(member)
    if new_acc:
        response.add_field(name='❕ Account Is New', value=f'Made {diff_msg.title()}', inline=True)
    else:
        response.add_field(name='🕑 Account Created', value=f'{diff_msg.title()}', inline=True)
    response.set_footer(text=f'UserID: {member.id}')
    await log_event(ev.db, member.guild, response)
