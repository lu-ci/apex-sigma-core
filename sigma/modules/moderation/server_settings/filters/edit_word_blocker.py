import discord

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.server_bound_logging import log_event
from .cleaners import clean_content


async def edit_word_blocker(ev, before, after):
    if after.guild:
        if isinstance(after.author, discord.Member):
            prefix = await ev.bot.get_prefix(after)
            if not after.content.startswith(prefix):
                text = clean_content(after.content.lower())
                elements = text.split(' ')
                blocked_words = await ev.db.get_guild_settings(after.guild.id, 'BlockedWords')
                if blocked_words is None:
                    blocked_words = []
                remove = False
                reason = None
                for word in blocked_words:
                    if word in elements:
                        remove = True
                        reason = word
                        break
                if remove:
                    try:
                        await after.delete()
                        title = f'🔥 Your message was deleted for containing "{reason}".'
                        to_author = discord.Embed(color=0xFFCC4D, title=title)
                        try:
                            await after.author.send(embed=to_author)
                        except discord.Forbidden:
                            pass
                        author = f'{after.author.name}#{after.author.discriminator}'
                        title = f'I deleted {author}\'s message for containing "{reason}".'
                        log_embed = discord.Embed(color=0xFFCC4D)
                        log_embed.set_author(name=title, icon_url=user_avatar(after.author))
                        await log_event(ev.db, after.guild, log_embed)
                    except discord.ClientException:
                        pass
