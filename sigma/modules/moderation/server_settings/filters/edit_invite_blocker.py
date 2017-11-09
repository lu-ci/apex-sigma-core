import discord

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.server_bound_logging import log_event


async def edit_invite_blocker(ev, before, after):
    if after.guild:
        if isinstance(after.author, discord.Member):
            if not after.author.permissions_in(after.channel).manage_guild:
                active = ev.db.get_guild_settings(after.guild.id, 'BlockInvites')
                if active is None:
                    active = False
                if active:
                    arguments = after.content.split(' ')
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
                        await after.delete()
                        try:
                            await after.author.send(embed=response)
                        except discord.Forbidden:
                            pass
                        log_embed = discord.Embed(color=0xF9F9F9)
                        author = f'{after.author.name}#{after.author.discriminator}'
                        log_embed.set_author(name=f'I removed {author}\'s invite link.',
                                             icon_url=user_avatar(after.author))
                        log_embed.set_footer(
                            text=f'Posted In: #{after.channel.name} | Leads To: {invite_found.guild.name}')
                        await log_event(ev.db, after.guild, log_embed)
