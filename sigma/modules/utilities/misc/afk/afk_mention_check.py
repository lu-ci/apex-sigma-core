import asyncio

import arrow
import discord


async def afk_mention_check(ev, message):
    if message.guild:
        pfx = await ev.bot.get_prefix(message)
        if not message.content.startswith(pfx):
            if message.mentions:
                target = message.mentions[0]
                afk_data = await ev.db[ev.db.db_cfg.database]['AwayUsers'].find_one({'UserID': target.id})
                if afk_data:
                    time_then = arrow.get(afk_data['Timestamp'])
                    afk_time = arrow.get(time_then).humanize(arrow.utcnow()).title()
                    afk_reason = afk_data['Reason']
                    url = None
                    for piece in afk_reason.split():
                        if piece.startswith('http'):
                            suffix = piece.split('.')[-1]
                            if suffix in ['gif', 'jpg', 'jpeg', 'png']:
                                afk_reason = afk_reason.replace(piece, '')
                                url = piece
                                break
                    response = discord.Embed(color=0x3B88C3, timestamp=time_then.datetime)
                    response.add_field(name=f'ℹ {target.name} is AFK.',
                                       value=f'Reason: {afk_reason}\nWent AFK: {afk_time}')
                    if url:
                        response.set_image(url=url)
                    afk_notify = await message.channel.send(embed=response)
                    await asyncio.sleep(5)
                    try:
                        await afk_notify.delete()
                    except discord.NotFound:
                        pass
