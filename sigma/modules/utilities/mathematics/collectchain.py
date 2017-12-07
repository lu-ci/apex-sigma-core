import arrow
import discord

from sigma.core.utilities.data_processing import user_avatar

in_use = False
in_use_by = None


def check_for_bot_prefixes(prefix, text):
    common_pfx = [prefix, '!', '/', '\\', '~', '.', '>', '-', '_', '?']
    prefixed = False
    for pfx in common_pfx:
        if text.startswith(pfx):
            prefixed = True
            break
    return prefixed


# noinspection PyBroadException
async def collectchain(cmd, message, args):
    global in_use
    global in_use_by
    if in_use:
        response = discord.Embed(color=0x696969, title='🛠 Currently in use. Try Again Later.')
        response.set_author(name=f'{in_use_by.name}', icon_url=user_avatar(in_use_by))
        await message.channel.send(None, embed=response)
    else:
        if message.mentions:
            target = message.mentions[0]
        else:
            if args:
                target = discord.utils.find(lambda x: x.name.lower() == ' '.join(args).lower(), message.guild.members)
            else:
                target = message.author
        if target:
            if not target.bot:
                start_time = arrow.utcnow().timestamp
                if message.channel_mentions:
                    target_chn = message.channel_mentions[0]
                else:
                    target_chn = message.channel
                collected = 0
                collection = await cmd.db[cmd.db.db_cfg.database]['MarkovChains'].find_one({'UserID': target.id})
                if collection:
                    collection = collection['Chain']
                else:
                    collection = []
                in_use = True
                in_use_by = message.author
                ch_response = discord.Embed(color=0x66CC66,
                                            title='📖 Collecting... You will be sent a DM when I\'m done.')
                await message.channel.send(None, embed=ch_response)
                try:
                    async for log in target_chn.history(limit=100000):
                        if log.author.id == target.id:
                            if log.content:
                                if log.content != '':
                                    if len(log.content) > 3:
                                        if not check_for_bot_prefixes(cmd.bot.get_prefix(message), log.content):
                                            if 'http' not in log.content and '```' not in log.content:
                                                if '"' not in log.content:
                                                    content = log.content
                                                    if log.mentions:
                                                        for mention in log.mentions:
                                                            content = content.replace(mention.mention, mention.name)
                                                    if log.channel_mentions:
                                                        for mention in log.channel_mentions:
                                                            content = content.replace(mention.mention, mention.name)
                                                    unallowed_chars = ['`', '\n', '\\', '\\n']
                                                    for char in unallowed_chars:
                                                        content = content.replace(char, '')
                                                    if len(content) > 12:
                                                        if not content.endswith(('.' or '?' or '!')):
                                                            content += '.'
                                                    if content not in collection:
                                                        collection.append(content)
                                                        collected += 1
                                                        if collected >= 5000:
                                                            break
                except Exception:
                    pass
                await cmd.db[cmd.db.db_cfg.database]['MarkovChains'].delete_one({'UserID': target.id})
                data = {
                    'UserID': target.id,
                    'Chain': collection
                }
                await cmd.db[cmd.db.db_cfg.database]['MarkovChains'].insert_one(data)
                in_use = False
                in_use_by = None
                dm_response = discord.Embed(color=0x66CC66, title=f'📖 {target.name}\'s chain is done!')
                dm_response.add_field(name='Amount Collected', value=f'```\n{collected}\n```')
                dm_response.add_field(name='Total Amount', value=f'```\n{len(collection)}\n```')
                dm_response.add_field(name='Time Elapsed', value=f'```\n{arrow.utcnow().timestamp - start_time}s\n```')
                try:
                    await message.author.send(None, embed=dm_response)
                except discord.Forbidden:
                    pass
                await message.channel.send(None, embed=dm_response)
                if message.author.id != target.id:
                    tgt_msg = discord.Embed(color=0x66CC66,
                                            title=f'📖 {message.author.name} has made a markov chain for you.')
                    try:
                        await target.send(None, embed=tgt_msg)
                    except discord.Forbidden:
                        pass
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Nope, no bot chains allowed.')
                await message.channel.send(embed=response)
