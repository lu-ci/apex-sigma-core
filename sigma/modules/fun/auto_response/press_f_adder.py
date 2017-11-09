async def press_f_adder(ev, message):
    if message.content.lower() == 'f':
        if message.guild:
            respond = ev.db.get_guild_settings(message.guild.id, 'AutoResponder')
            if respond:
                if message.guild.me.permissions_in(message.channel).add_reactions:
                    await message.add_reaction('🇫')
