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

import re

import discord

from sigma.core.mechanics.permissions import ServerCommandPermissions
from sigma.core.utilities.data_processing import command_message_parser


def escape_mentions(text, guild):
    """
    :type text: str
    :type guild: discord.Guild
    :rtype: str
    """
    if guild is not None:
        role_ids = re.findall(r'<@&([0-9]+)>', text)
        for role_id in role_ids:
            role = guild.get_role(int(role_id))
            role_name = f'@\u200b{role.name}' if role else '@\u200bunknown'
            text = text.replace(f'<@&{role_id}>', role_name)

    text = text.replace('@everyone', '@\u200beveryone')
    text = text.replace('@here', '@\u200bhere')
    return text


def log_command_usage(log, message, command):
    """
    :type log: sigma.core.mechanics.logger.Logger
    :type message: discord.Message
    :type command: str
    """
    if message.guild:
        cmd_location = f'SRV: {message.guild.name} [{message.guild.id}] | '
        cmd_location += f'CHN: #{message.channel.name} [{message.channel.id}]'
    else:
        cmd_location = 'DIRECT MESSAGE'
    author_full = f'{message.author.name}#{message.author.discriminator} [{message.author.id}]'
    log_text = f'USR: {author_full} | {cmd_location} | CMD: {command}'
    log.info(log_text)


async def custom_command(ev, pld):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :param pld: The event payload data to process.
    :type pld: sigma.core.mechanics.payload.MessagePayload
    """
    if pld.msg.guild:
        prefix = ev.db.get_prefix(pld.settings)
        if pld.msg.content.startswith(prefix):
            if pld.msg.content != prefix and not pld.msg.content.startswith(prefix + ' '):
                cmd = pld.msg.content[len(prefix):].lower().split()[0]
                if cmd not in ev.bot.modules.commands and cmd not in ev.bot.modules.alts:
                    perms = ServerCommandPermissions(ev, pld.msg)
                    await perms.check_perms()
                    if perms.permitted:
                        custom_commands = pld.settings.get('custom_commands')
                        if custom_commands is None:
                            custom_commands = {}
                        if cmd in custom_commands:
                            delcmd = pld.settings.get('delete_commands')
                            if delcmd:
                                try:
                                    await pld.msg.delete()
                                except (discord.NotFound, discord.Forbidden):
                                    pass
                            cmd_text = custom_commands[cmd]
                            img = False
                            if cmd_text.startswith('http'):
                                img_endings = ['.gif', '.png', '.jpg', '.jpeg']
                                for ending in img_endings:
                                    if cmd_text.endswith(ending):
                                        img = True
                                        break
                            if img:
                                response = discord.Embed().set_image(url=cmd_text)
                                await pld.msg.channel.send(embed=response)
                            else:
                                response = command_message_parser(pld.msg, cmd_text)
                                await pld.msg.channel.send(escape_mentions(response, pld.msg.guild))
                            log_command_usage(ev.log, pld.msg, cmd)
