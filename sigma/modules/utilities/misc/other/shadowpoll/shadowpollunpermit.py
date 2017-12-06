import discord


async def shadowpollunpermit(cmd, message, args):
    if args:
        if len(args) >= 2:
            poll_id = args[0].lower()
            if message.mentions:
                perm_type = 'users'
                target = message.mentions[0]
                if not isinstance(target, discord.Member):
                    target = None
            elif message.channel_mentions:
                perm_type = 'channels'
                target = message.channel_mentions[0]
            else:
                lookup = ' '.join(args[1:]).lower()
                perm_type = 'roles'
                target = discord.utils.find(lambda x: x.name.lower() == lookup, message.guild.roles)
            if target:
                poll_file = cmd.db[cmd.db.db_cfg.database].ShadowPolls.find_one({'id': poll_id})
                if poll_file:
                    author = poll_file['origin']['author']
                    if author == message.author.id:
                        if target.id in poll_file['permissions'][perm_type]:
                            poll_file['permissions'][perm_type].remove(target.id)
                            cmd.db[cmd.db.db_cfg.database].ShadowPolls.update_one({'id': poll_id}, {'$set': poll_file})
                            response = discord.Embed(color=0x66CC66, title=f'✅ {target.name} has been unpermitted.')
                        else:
                            response = discord.Embed(color=0xBE1931, title=f'❗ {target.name} is not permitted.')
                    else:
                        response = discord.Embed(color=0xBE1931, title='⛔ You didn\'t make this poll.')
                else:
                    response = discord.Embed(color=0x696969, title='🔍 I couldn\'t find that poll.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Target not located.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Missing permission target.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Missing poll ID and target.')
    await message.channel.send(embed=response)
