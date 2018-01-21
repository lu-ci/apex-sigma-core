import discord


async def wipechain(cmd: SigmaCommand, message: discord.Message, args: list):
    uid = message.author.id
    exist_check = await cmd.db[cmd.db.db_cfg.database].MarkovChains.find_one({'UserID': uid})
    if exist_check:
        chain_len = len(exist_check['Chain'])
        await cmd.db[cmd.db.db_cfg.database].MarkovChains.delete_one({'UserID': uid})
        response = discord.Embed(color=0x66CC66, title=f'✅ Your chain of {chain_len} items has been wiped.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ You don\'t have a Markov Chain.')
    await message.channel.send(embed=response)
