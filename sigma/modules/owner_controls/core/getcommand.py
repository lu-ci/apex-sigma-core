import arrow
import discord


async def getcommand(cmd, message, args):
    if args:
        lookup = ''.join(args).lower()
        command_file = await cmd.db[cmd.db.db_cfg.database].CommandStats.find_one({'id': lookup})
        if command_file:
            auth_name = command_file['author']
            auth_member = discord.utils.find(lambda x: x.id == auth_name, cmd.bot.get_all_members())
            if auth_member:
                auth_name = f'{auth_member.name}#{auth_member.discriminator}'
            chan_name = command_file['channel']
            if chan_name:
                chan_obj = discord.utils.find(lambda x: x.id == chan_name, cmd.bot.get_all_channels())
                if chan_name:
                    chan_name = f'#{chan_obj.name}'
            else:
                chan_name = 'DM'
            gild_name = command_file['guild']
            if gild_name:
                gild_obj = discord.utils.find(lambda x: x.id == gild_name, cmd.bot.guilds)
                if gild_obj:
                    gild_name = gild_obj.name
            else:
                gild_name = 'DM'
            gen_text = f'Command: {command_file["command"]}'
            gen_text += f'\nTimestamp: {command_file["timestamp"]}'
            gen_text += f'\nTime: {arrow.get(command_file["timestamp"]).format("DD. MMM. YYYY HH:MM:SS")}'
            aut_text = f'Author: {auth_name}'
            aut_text += f'\nChannel: {chan_name}'
            aut_text += f'\nGuild: {gild_name}'
            response = discord.Embed(color=0xF9F9F9, title=f'Command: {command_file["id"]}')
            response.add_field(name='General', value=gen_text, inline=True)
            response.add_field(name='Author', value=aut_text, inline=True)
            response.add_field(name='Arguments', value=' '.join(command_file["args"]), inline=False)
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Command ID not found.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ No token inputted.')
    await message.channel.send(embed=response)
