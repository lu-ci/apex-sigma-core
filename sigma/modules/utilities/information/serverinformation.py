from sigma.core.mechanics.command import SigmaCommand
import arrow
import discord


async def serverinformation(cmd: SigmaCommand, message: discord.Message, args: list):
    gld = message.guild
    own = gld.owner
    response = discord.Embed(color=0x1B6F5F)
    response.set_author(name=gld.name, icon_url=gld.icon_url)
    creation_time = arrow.get(gld.created_at).format('DD. MMMM YYYY')
    bot_count = 0
    user_count = 0
    for user in gld.members:
        if user.bot:
            bot_count += 1
        else:
            user_count += 1
    guild_text = f'Name: **{gld.name}**'
    guild_text += f'\nID: **{gld.id}**'
    guild_text += f'\nMembers: **{user_count}**'
    guild_text += f'\nBots: **{bot_count}**'
    guild_text += f'\nChannels: **{len(gld.channels)}**'
    guild_text += f'\nRoles: **{len(gld.roles)}**'
    guild_text += f'\nCreated: **{creation_time}**'
    response.add_field(name='Guild Info', value=guild_text)
    own_creation_time = arrow.get(own.created_at).format('DD. MMMM YYYY')
    own_text = f'Username: **{own.name}**#{own.discriminator}'
    own_text += f'\nNickname: **{own.display_name}**'
    own_text += f'\nID: **{own.id}**'
    own_text += f'\nStatus: **{str(own.status).replace("dnd", "busy").title()}**'
    own_text += f'\nColor: **{str(own.color).upper()}**'
    own_text += f'\nTop Role: **{own.top_role.name}**'
    own_text += f'\nCreated: **{own_creation_time}**'
    response.add_field(name='Owner Info', value=own_text)
    if gld.afk_channel:
        detail_text = f'AFK Channel: **{gld.afk_channel.name}**'
        detail_text += f'\nAFK Timeout: **{gld.afk_timeout}**'
    else:
        detail_text = 'AFK Channel: **None**'
        detail_text += '\nAFK Timeout: **None**'
    detail_text += f'\nEmojis: **{len(gld.emojis)}**'
    detail_text += f'\nLarge: **{gld.large}**'
    detail_text += f'\nRegion: **{gld.region.name.upper()}**'
    detail_text += f'\nShard: **{gld.shard_id}**'
    detail_text += f'\nVerification: **{gld.verification_level.name.upper()}**'
    response.add_field(name='Details', value=detail_text)
    await message.channel.send(None, embed=response)
