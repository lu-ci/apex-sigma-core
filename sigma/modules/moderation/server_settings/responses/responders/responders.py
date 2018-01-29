import discord

from sigma.core.utilities.data_processing import get_image_colors


async def responders(cmd, message, args):
    responder_files = await cmd.db.get_guild_settings(message.guild.id, 'ResponderTriggers')
    if responder_files:
        if args:
            page = args[0]
            try:
                page = int(page)
            except ValueError:
                page = 1
        else:
            page = 1
        responder_list = sorted(list(responder_files.keys()))
        resp_count = len(responder_list)
        if page < 1:
            page = 1
        start_range = 10 * (page - 1)
        end_range = 10 * page
        triggers = responder_list[start_range:end_range]
        if triggers:
            if resp_count > 1:
                ender = 's'
            else:
                ender = ''
            summary = f'Showing **{len(triggers)}** trigger{ender} from Page **#{page}**.'
            summary += f'\n{message.guild.name} has **{resp_count}** responder trigger{ender}.'
            loop_index = start_range
            trg_list_lines = []
            for key in triggers:
                loop_index += 1
                list_line = f'**{loop_index}**: {key}'
                trg_list_lines.append(list_line)
            trg_list = '\n'.join(trg_list_lines)
            srv_color = await get_image_colors(message.guild.icon_url)
            response = discord.Embed(color=srv_color)
            response.set_author(name='Automatic Responder Triggers', icon_url=message.guild.icon_url)
            response.add_field(name='Summary', value=summary, inline=False)
            response.add_field(name='Trigger List', value=trg_list, inline=False)
        else:
            response = discord.Embed(title='❗ This page is empty.', color=0xBE1931)
    else:
        response = discord.Embed(title='❗ This server has no responder triggers.', color=0xBE1931)
    await message.channel.send(embed=response)
