import asyncio

import discord


def sigma_mention_check(mentions, sigma_id):
    sigma_present = False
    if mentions:
        for mention in mentions:
            if mention.id == sigma_id:
                sigma_present = True
    return sigma_present


async def afk_comeback_check(ev, message):
    if message.guild:
        if not message.content.startswith(ev.bot.get_prefix(message)):
            if not sigma_mention_check(message.mentions, ev.bot.user.id):
                afk_data = ev.db[ev.db.db_cfg.database]['AwayUsers'].find_one({'UserID': message.author.id})
                if afk_data:
                    ev.db[ev.db.db_cfg.database]['AwayUsers'].delete_one({'UserID': message.author.id})
                    response = discord.Embed(color=0x3B88C3, title='ℹ I have removed your AFK status.')
                    removal = await message.channel.send(embed=response)
                    await asyncio.sleep(5)
                    try:
                        await removal.delete()
                    except discord.ClientException:
                        pass
