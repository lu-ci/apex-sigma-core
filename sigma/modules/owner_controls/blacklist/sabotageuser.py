import discord


async def sabotageuser(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        target_id = ''.join(args)
        try:
            target_id = int(target_id)
            valid_id = True
        except ValueError:
            valid_id = False
        if valid_id:
            target = discord.utils.find(lambda x: x.id == target_id, cmd.bot.get_all_members())
            if target:
                sabotage_collection = cmd.db[cmd.bot.cfg.db.database].SabotagedUsers
                sabotage_file = await sabotage_collection.find_one({'UserID': target.id})
                if sabotage_file:
                    await cmd.db[cmd.bot.cfg.db.database].SabotagedUsers.delete_one({'UserID': target.id})
                    result = 'unsabotaged'
                    icon = '🔓'
                else:
                    await cmd.db[cmd.bot.cfg.db.database].SabotagedUsers.insert_one({'UserID': target.id})
                    result = 'sabotaged'
                    icon = '🔒'
                title = f'{icon} {target.name} has been {result}.'
                response = discord.Embed(color=0xFFCC4D, title=title)
            else:
                response = discord.Embed(color=0x696969, title='🔍 No user with that ID was found.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Invalid User ID.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ No User ID was inputted.')
    await message.channel.send(embed=response)
