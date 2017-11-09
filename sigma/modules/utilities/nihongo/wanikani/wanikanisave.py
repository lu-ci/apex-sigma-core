import discord


async def wanikanisave(cmd, message, args):
    try:
        await message.delete()
    except discord.ClientException:
        pass
    if args:
        api_key = ''.join(args)
        api_document = cmd.db[cmd.db.db_cfg.database]['WaniKani'].find_one({'UserID': message.author.id})
        data = {'UserID': message.author.id, 'WKAPIKey': api_key}
        if api_document:
            ender = 'updated'
            cmd.db[cmd.db.db_cfg.database]['WaniKani'].update_one({'UserID': message.author.id}, {'$set': data})
        else:
            ender = 'saved'
            cmd.db[cmd.db.db_cfg.database]['WaniKani'].insert_one(data)
        response = discord.Embed(color=0x66CC66, title=f'🔑 Your key has been {ender}.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
