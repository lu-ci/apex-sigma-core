import discord


async def shadowpolldelete(cmd, message, args):
    if args:
        poll_id = args[0].lower()
        poll_file = cmd.db[cmd.db.db_cfg.database].ShadowPolls.find_one({'id': poll_id})
        if poll_file:
            author = poll_file['origin']['author']
            if author == message.author.id:
                cmd.db[cmd.db.db_cfg.database].ShadowPolls.delete_one({'id': poll_id})
                response = discord.Embed(color=0x66CC66, title=f'✅ Poll {poll_id} has been deleted.')
            else:
                response = discord.Embed(color=0xBE1931, title='⛔ You didn\'t make this poll.')
        else:
            response = discord.Embed(color=0x696969, title='🔍 I couldn\'t find that poll.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Missing poll ID.')
    await message.channel.send(embed=response)
