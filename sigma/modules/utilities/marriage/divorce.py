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

import arrow
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import error


async def send_divorce(author: discord.Member, target: discord.Member, is_divorce):
    """

    :param author:
    :type author:
    :param target:
    :type target:
    :param is_divorce:
    :type is_divorce:
    """
    if is_divorce:
        splitup = discord.Embed(color=0xe75a70, title=f'💔 {author.name} has divorced you...')
    else:
        splitup = discord.Embed(color=0xe75a70, title=f'💔 {author.name} has canceled the proposal...')
    try:
        await target.send(embed=splitup)
    except discord.Forbidden:
        pass


async def divorce(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    target = None
    is_id = False
    tid = None
    if pld.msg.mentions:
        target = pld.msg.mentions[0]
        tid = target.id
    else:
        if pld.args:
            try:
                target = tid = int(pld.args[0])
                is_id = True
            except ValueError:
                target = None
    if tid:
        if tid != pld.msg.author.id:
            a_spouses = await cmd.bot.db.get_profile(pld.msg.author.id, 'spouses') or []
            a_spouse_ids = [s.get('user_id') for s in a_spouses]
            if is_id:
                t_spouses = await cmd.db.get_profile(target, 'spouses') or []
            else:
                t_spouses = await cmd.db.get_profile(target.id, 'spouses') or []
            t_spouse_ids = [s.get('user_id') for s in t_spouses]
            if pld.msg.author.id in t_spouse_ids and tid in a_spouse_ids:
                current_kud = await cmd.db.get_resource(pld.msg.author.id, 'currency')
                current_kud = current_kud.current
                marry_stamp = discord.utils.find(lambda s: s.get('user_id') == tid, a_spouses).get('time')
                time_diff = arrow.utcnow().timestamp - marry_stamp
                div_cost = int(time_diff * 0.004)
                if current_kud >= div_cost:
                    for sp in a_spouses:
                        if is_id:
                            if sp.get('user_id') == target:
                                a_spouses.remove(sp)
                        else:
                            if sp.get('user_id') == target.id:
                                a_spouses.remove(sp)
                    for sp in t_spouses:
                        if sp.get('user_id') == pld.msg.author.id:
                            t_spouses.remove(sp)
                    await cmd.db.set_profile(pld.msg.author.id, 'spouses', a_spouses)
                    if is_id:
                        await cmd.db.set_profile(target, 'spouses', t_spouses)
                    else:
                        await cmd.db.set_profile(target.id, 'spouses', t_spouses)
                    if is_id:
                        div_title = f'💔 You have divorced {target}...'
                    else:
                        div_title = f'💔 You have divorced {target.name}...'
                    response = discord.Embed(color=0xe75a70, title=div_title)
                    if not is_id:
                        await send_divorce(pld.msg.author, target, True)
                    await cmd.db.del_resource(pld.msg.author.id, 'currency', div_cost, cmd.name, pld.msg)
                else:
                    currency = cmd.bot.cfg.pref.currency
                    response = error(f'You don\'t have {div_cost} {currency} to get a divorce.')
            else:
                if is_id:
                    response = error(f'You aren\'t married to {target}.')
                else:
                    response = error(f'You aren\'t married to {target.name}.')
        else:
            response = error('Can\'t divorce yourself.')
    else:
        response = error('No user targeted.')
    await pld.msg.channel.send(embed=response)
