from .auto_responder import clean_word


async def auto_reactor(ev, message):
    if message.guild:
        if message.content:
            pfx = await ev.bot.get_prefix(message)
            if not message.content.startswith(pfx):
                triggers = await ev.db.get_guild_settings(message.guild.id, 'ReactorTriggers') or {}
                arguments = message.content.split(' ')
                for arg in arguments:
                    arg = clean_word(arg)
                    if arg in triggers:
                        reaction = triggers[arg]
                        try:
                            await message.add_reaction(reaction)
                        except Exception:
                            pass
                        break
