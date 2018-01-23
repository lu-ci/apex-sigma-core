async def experience_activity(ev, message):
    if message.guild:
        if not await ev.bot.cool_down.on_cooldown(ev.name, message.author):
            if len(message.guild.members) >= 100:
                award_xp = 180
            else:
                award_xp = 150
            await ev.db.add_experience(message.author, message.guild, award_xp)
            await ev.bot.cool_down.set_cooldown(ev.name, message.author, 80)
