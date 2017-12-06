import discord


async def shadowpollclose(cmd, message, args):
    if args:
        poll_id = args[0].lower()
        poll_file = cmd.db[cmd.db.db_cfg.database].ShadowPolls.find_one({'id': poll_id})
        if poll_file:
            author = poll_file['origin']['author']
            if author == message.author.id:
                active = poll_file['settings']['active']
                if active:
                    poll_file['settings'].update({'active': False})
                    cmd.db[cmd.db.db_cfg.database].ShadowPolls.update_one({'id': poll_id}, {'$set': poll_file})
                    response = discord.Embed(color=0xFFCC4D, title=f'🔒 Poll {poll_file["id"]} has been closed.')
                else:
                    response = discord.Embed(color=0xBE1931, title=f'❗ Poll {poll_file["id"]} is not active.')
            else:
                response = discord.Embed(color=0xBE1931, title='⛔ You didn\'t make this poll.')
        else:
            response = discord.Embed(color=0x696969, title='🔍 I couldn\'t find that poll.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Missing poll ID.')
    await message.channel.send(embed=response)
