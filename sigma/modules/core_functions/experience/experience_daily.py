async def experience_daily(ev, message):
    if message.guild:
        if not await ev.bot.cool_down.on_cooldown(ev.name, message.author):
            if len(message.guild.members) >= 100:
                award_xp = 1800
            else:
                award_xp = 1500
            await ev.db.add_experience(message.author, message.guild, award_xp)
            await ev.bot.cool_down.set_cooldown(ev.name, message.author, 85000)

