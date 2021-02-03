"""
Apex Sigma: The Database Giant Discord Bot.
Copyright (C) 2019  Lucia's Cipher

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import secrets

import arrow
import discord

from sigma.core.utilities.data_processing import convert_to_seconds, get_image_colors, user_avatar
from sigma.core.utilities.generic_responses import GenericResponse

raffle_icons = ['⭐', '💎', '🎉', '🎁', '📥']
icon_colors = {'⭐': 0xffac33, '💎': 0x5dadec, '🎉': 0xdd2e44, '🎁': 0xfdd888, '📥': 0x77b255}


async def raffle(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if len(pld.args) >= 2:
        time_input = pld.args[0]
        try:
            time_sec = convert_to_seconds(time_input)
            start_stamp = arrow.utcnow().float_timestamp
            end_stamp = start_stamp + time_sec
            end_dt = arrow.get(end_stamp).datetime
            if time_sec < 90:
                end_hum = f'in {time_sec} seconds'
            else:
                end_hum = arrow.get(end_stamp).humanize()
            rafid = secrets.token_hex(3)
            reaction_name = reaction_icon = pld.settings.get('raffle_icon')
            icon_color = None
            if reaction_icon:
                gld = pld.msg.guild
                guild_icon = str(gld.icon_url) if gld.icon_url else discord.Embed.Empty
                custom_emote = reaction_icon.startswith('<:') and reaction_icon.endswith('>')
                if custom_emote:
                    emote_name = reaction_icon.split(':')[1]
                    matching_emote = None
                    for emote in pld.msg.guild.emojis:
                        if emote.name == emote_name:
                            matching_emote = emote
                    if not matching_emote:
                        reaction_icon = None
                        await cmd.db.set_guild_settings(pld.msg.guild.id, 'raffle_icon', None)
                    else:
                        reaction_icon = matching_emote
                        icon_color = await get_image_colors(matching_emote.url)
                else:
                    icon_color = await get_image_colors(guild_icon)
            if not reaction_icon:
                reaction_name = reaction_icon = secrets.choice(raffle_icons)
                icon_color = icon_colors.get(reaction_icon)
            resp_title = f'{pld.msg.author.display_name} started a raffle!'
            target_ch = pld.msg.channel_mentions[0] if pld.msg.channel_mentions else pld.msg.channel
            external = pld.msg.channel.id != target_ch.id
            draw_count = 1
            args = [a.lower() for a in pld.args]
            automatic = False
            for arg in args:
                if arg.startswith('winners:'):
                    pld.args.pop(args.index(arg))
                    draw_num = arg.split(':')[-1]
                    if draw_num.isdigit():
                        draw_count = int(draw_num)
                if arg.lower() == 'automatic':
                    pld.args.pop(args.index(arg))
                    if pld.msg.author.id in cmd.bot.cfg.dsc.owners:
                        automatic = True
            if external:
                allowed = pld.msg.author.permissions_in(target_ch).send_messages
                if allowed:
                    for ai, arg in enumerate(pld.args):
                        if arg == target_ch.mention:
                            pld.args.pop(ai)
            else:
                allowed = True
            if allowed:
                raffle_title = ' '.join(pld.args[1:])
                starter = discord.Embed(color=icon_color, timestamp=end_dt)
                starter.set_author(name=resp_title, icon_url=user_avatar(pld.msg.author))
                starter.description = f'Prize: **{raffle_title}**'
                if draw_count > 1:
                    starter.description += f'\nWinners: **{draw_count}**'
                starter.description += f'\nReact with a {reaction_icon} to enter the raffle.'
                starter.set_footer(text=f'[{rafid}] Raffle ends {end_hum}.')
                starter_message = await target_ch.send(embed=starter)
                await starter_message.add_reaction(reaction_icon)
                raffle_data = {
                    'automatic': automatic,
                    'author': pld.msg.author.id,
                    'channel': target_ch.id,
                    'title': raffle_title,
                    'start': start_stamp,
                    'end': end_stamp,
                    'icon': reaction_name,
                    'color': icon_color,
                    'draw_count': draw_count,
                    'message': starter_message.id,
                    'active': True,
                    'id': rafid
                }
                await cmd.db[cmd.db.db_nam].Raffles.insert_one(raffle_data)
                response = None
            else:
                response = GenericResponse(f'You can\'t send messages to #{target_ch.name}.').denied()
        except (LookupError, ValueError):
            response = GenericResponse('Please use the format HH:MM:SS.').error()
    else:
        response = GenericResponse('Nothing inputted.').error()
    if response:
        await pld.msg.channel.send(embed=response)
