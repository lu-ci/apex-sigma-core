import discord

from sigma.core.utilities.data_processing import user_avatar


async def send_invite_blocker(ev, message):
    if message.guild:
        if isinstance(message.author, discord.Member):
            if not message.author.permissions_in(message.channel).manage_guild:
                active = await ev.db.get_guild_settings(message.guild.id, 'BlockInvites')
                if active is None:
                    active = False
                if active:
                    arguments = message.content.split(' ')
                    invite_found = False
                    for arg in arguments:
                        triggers = ['.gg', '.com', 'http']
                        for trigger in triggers:
                            if trigger in arg:
                                try:
                                    invite_found = await ev.bot.get_invite(arg)
                                    break
                                except discord.NotFound:
                                    pass
                    if invite_found:
                        title = '⛓ Invite links are not allowed on this server.'
                        response = discord.Embed(color=0xF9F9F9, title=title)
                        await message.delete()
                        try:
                            await message.author.send(embed=response)
                        except discord.Forbidden:
                            pass
                        log_embed = discord.Embed(color=0xF9F9F9)
                        author = f'{message.author.name}#{message.author.discriminator}'
                        log_embed.set_author(name=f'I removed {author}\'s invite link.',
                                             icon_url=user_avatar(message.author))
                        log_embed.set_footer(
                            text=f'Posted In: #{message.channel.name} | Leads To: {invite_found.guild.name}')
                        await log_event(ev.db, message.guild, log_embed)
