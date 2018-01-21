import discord


async def blacklistuser(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        target_id = args[0]
        try:
            target_id = int(target_id)
            valid_id = True
        except ValueError:
            valid_id = False
        if valid_id:
            target = discord.utils.find(lambda x: x.id == target_id, cmd.bot.get_all_members())
            if target:
                black_user_collection = cmd.db[cmd.bot.cfg.db.database].BlacklistedUsers
                black_user_file = await black_user_collection.find_one({'UserID': target.id})
                if black_user_file:
                    if black_user_file.get('Total'):
                        update_data = {'$set': {'UserID': target.id, 'Total': False}}
                        icon = '🔓'
                        result = 'removed from the blacklist'
                    else:
                        update_data = {'$set': {'UserID': target.id, 'Total': True}}
                        icon = '🔒'
                        result = 'blacklisted'
                    await black_user_collection.update_one({'UserID': target.id}, update_data)
                else:
                    await black_user_collection.insert_one({'UserID': target.id, 'Total': True})
                    result = 'blacklisted'
                    icon = '🔒'
                title = f'{icon} {target.name}#{target.discriminator} has been {result}.'
                response = discord.Embed(color=0xFFCC4D, title=title)
            else:
                response = discord.Embed(color=0x696969, title='🔍 No user with that ID was found.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Invalid User ID.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ No User ID was inputted.')
    await message.channel.send(embed=response)
