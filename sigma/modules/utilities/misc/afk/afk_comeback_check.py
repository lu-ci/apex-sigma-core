import asyncio

import discord


def sigma_mention_check(content, sigma_id):
    sigma_present = False
    if content:
        first_arg = content.split(' ')[0]
        if first_arg.startswith('<@') and first_arg.endswith('>'):
            try:
                uid = int(first_arg[2:-1])
                if uid == sigma_id:
                    sigma_present = True
            except ValueError:
                uid = None
            except IndexError:
                uid = None
    return sigma_present


async def afk_comeback_check(ev, message):
    if message.guild:
        pfx = await ev.bot.get_prefix(message)
        if not message.content.startswith(pfx):
            if not sigma_mention_check(message.content, ev.bot.user.id):
                afk_data = await ev.db[ev.db.db_cfg.database]['AwayUsers'].find_one({'UserID': message.author.id})
                if afk_data:
                    await ev.db[ev.db.db_cfg.database]['AwayUsers'].delete_one({'UserID': message.author.id})
                    response = discord.Embed(color=0x3B88C3, title='ℹ I have removed your AFK status.')
                    removal = await message.channel.send(embed=response)
                    await asyncio.sleep(5)
                    try:
                        await removal.delete()
                    except discord.ClientException:
                        pass
