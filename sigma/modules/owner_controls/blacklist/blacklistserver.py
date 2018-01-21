from sigma.core.mechanics.command import SigmaCommand
import discord


async def blacklistserver(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        target_id = ''.join(args)
        try:
            target_id = int(target_id)
            valid_id = True
        except ValueError:
            valid_id = False
        if valid_id:
            target = discord.utils.find(lambda x: x.id == target_id, cmd.bot.guilds)
            if target:
                black_user_collection = cmd.db[cmd.bot.cfg.db.database].BlacklistedServers
                black_user_file = await black_user_collection.find_one({'ServerID': target.id})
                if black_user_file:
                    await cmd.db[cmd.bot.cfg.db.database].BlacklistedServers.delete_one({'ServerID': target.id})
                    result = 'removed from the blacklist'
                    icon = '🔓'
                else:
                    await cmd.db[cmd.bot.cfg.db.database].BlacklistedServers.insert_one({'ServerID': target.id})
                    result = 'blacklisted'
                    icon = '🔒'
                title = f'{icon} {target.name} has been {result}.'
                response = discord.Embed(color=0xFFCC4D, title=title)
            else:
                response = discord.Embed(color=0x696969, title='🔍 No guild with that ID was found.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Invalid Guild ID.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ No Guild ID was inputted.')
    await message.channel.send(embed=response)
