import discord

from sigma.core.utilities.data_processing import user_avatar
from .cleaners import clean_content


async def send_word_blocker(ev, message):
    if message.guild:
        if isinstance(message.author, discord.Member):
            prefix = await ev.bot.get_prefix(message)
            if not message.content.startswith(prefix):
                text = clean_content(message.content.lower())
                elements = text.split(' ')
                blocked_words = await ev.db.get_guild_settings(message.guild.id, 'BlockedWords')
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
                        await message.delete()
                        title = f'🔥 Your message was deleted for containing "{reason}".'
                        to_author = discord.Embed(color=0xFFCC4D, title=title)
                        try:
                            await message.author.send(embed=to_author)
                        except discord.Forbidden:
                            pass
                        author = f'{message.author.name}#{message.author.discriminator}'
                        title = f'I deleted {author}\'s message for containing "{reason}".'
                        log_embed = discord.Embed(color=0xFFCC4D)
                        log_embed.set_author(name=title, icon_url=user_avatar(message.author))
                        await log_event(ev.db, message.guild, log_embed)
                    except discord.ClientException:
                        pass
