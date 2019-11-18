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

import datetime
import secrets

import arrow
import discord

from sigma.core.utilities.generic_responses import error


def check_name(m: discord.Member, lookup: str):
    """

    :param m:
    :type m:
    :param lookup:
    :type lookup:
    :return:
    :rtype:
    """
    return m.name.lower() == lookup.lower() or m.display_name.lower() == lookup.lower()


async def givecookie(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    someoned = False
    if pld.msg.mentions:
        target = pld.msg.mentions[0]
    else:
        if pld.args:
            if pld.args[0].lower() == '@someone':
                members = pld.msg.guild.members
                mid = pld.msg.author.id
                targets = [member for member in members if not (member.bot or member.id == mid)]
                if targets:
                    target = secrets.choice(targets)
                else:
                    target = None
                someoned = True
            else:
                lookup = ' '.join(pld.args)
                target = discord.utils.find(lambda m: check_name(m, lookup), pld.msg.guild.members)
        else:
            target = None
    if target:
        sabotage_target = await cmd.db.is_sabotaged(target.id)
        sabotage_author = await cmd.db.is_sabotaged(pld.msg.author.id)
        author_stamp = arrow.get(pld.msg.author.created_at).float_timestamp
        current_stamp = arrow.utcnow().float_timestamp
        time_diff = current_stamp - author_stamp
        if not sabotage_author:
            if not sabotage_target:
                if time_diff > 2592000:
                    if pld.msg.author.id != target.id:
                        if not target.bot:
                            if not await cmd.bot.cool_down.on_cooldown(cmd.name, pld.msg.author):
                                upgrade_file = await cmd.bot.db.get_profile(pld.msg.author.id, 'upgrades') or {}
                                base_cooldown = 3600
                                stamina = upgrade_file.get('oven') or 0
                                stamina_mod = stamina / (1.25 + (0.01 * stamina))
                                cooldown = int(base_cooldown - ((base_cooldown / 100) * stamina_mod))
                                await cmd.db.add_resource(target.id, 'cookies', 1, cmd.name, pld.msg, True)
                                await cmd.bot.cool_down.set_cooldown(cmd.name, pld.msg.author, cooldown)
                                if someoned:
                                    title = f'🍪 You threw a cookie and it landed in {target.display_name}\'s mouth.'
                                else:
                                    title = f'🍪 You gave a cookie to {target.display_name}.'
                                response = discord.Embed(color=0xd99e82, title=title)
                            else:
                                timeout_seconds = await cmd.bot.cool_down.get_cooldown(cmd.name, pld.msg.author)
                                if timeout_seconds > 60:
                                    timeout_seconds = arrow.utcnow().timestamp + timeout_seconds
                                    timeout = arrow.get(timeout_seconds).humanize()
                                else:
                                    timeout = f'in {timeout_seconds} seconds'
                                timeout_title = f'🕙 Your cookie will be baked {timeout}.'
                                response = discord.Embed(color=0x696969, title=timeout_title)
                        else:
                            response = error('Bots don\'t eat cookies.')
                    else:
                        response = error('Nope, can\'t give cookies to yourself.')
                else:
                    response = error('Sorry, your account is too young to give cookies.')
            else:
                response = error(f'It seems that {target.name} is allergic to cookies.')
        else:
            response = error('It seems that your oven is broken.')
    else:
        if not await cmd.bot.cool_down.on_cooldown(cmd.name, pld.msg.author):
            response = discord.Embed(color=0xd99e82, title='🍪 Your cookie is ready to be given.')
        else:
            timeout_seconds = await cmd.bot.cool_down.get_cooldown(cmd.name, pld.msg.author)
            if timeout_seconds > 3600:
                timeout_seconds = arrow.utcnow().timestamp + timeout_seconds
                timeout = arrow.get(timeout_seconds).humanize()
            elif timeout_seconds > 60:
                tdelta = str(datetime.timedelta(seconds=timeout_seconds)).split(':')[1]
                timeout = f'in {int(tdelta)} minutes'
            else:
                timeout = f'in {timeout_seconds} seconds'
            timeout_title = f'🕙 Your cookie will be baked {timeout}.'
            response = discord.Embed(color=0x696969, title=timeout_title)
    await pld.msg.channel.send(embed=response)
