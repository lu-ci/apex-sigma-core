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

import copy

import arrow
import discord

from sigma.core.utilities.dialogue_controls import DialogueCore
from sigma.core.utilities.generic_responses import error


def sync_spouses(spouses, user_id):
    """

    :param spouses:
    :type spouses: list[dict]
    :param user_id:
    :type user_id: int
    """
    for spouse in spouses:
        if spouse.get('user_id') == user_id:
            spouses.remove(spouse)
            break


async def marry(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.mentions:
        target = pld.msg.mentions[0]
        author = pld.msg.author
        if target.id != author.id:
            if not target.bot:
                fake_msg = copy.copy(pld.msg)
                fake_msg.author = target
                author_upgrades = await cmd.bot.db.get_profile(pld.msg.author.id, 'upgrades') or {}
                target_upgrades = await cmd.db.get_profile(target.id, 'upgrades') or {}
                author_limit = 10 + (author_upgrades.get('harem') or 0)
                target_limit = 10 + (target_upgrades.get('harem') or 0)
                a_spouses = await cmd.bot.db.get_profile(pld.msg.author.id, 'spouses') or []
                a_spouse_ids = [s.get('user_id') for s in a_spouses]
                t_spouses = await cmd.db.get_profile(target.id, 'spouses') or []
                t_spouse_ids = [s.get('user_id') for s in t_spouses]
                a_limited = True if len(a_spouses) >= author_limit else False
                t_limited = True if len(t_spouses) >= target_limit else False
                if not a_limited and not t_limited:
                    married = target.id in a_spouse_ids and pld.msg.author.id in t_spouse_ids
                    if not married:
                        proposal = discord.Embed(color=0xf9f9f9, title=f'💍 {target.name}, do you accept the proposal?')
                        dialogue = DialogueCore(cmd.bot, fake_msg, proposal)
                        dresp = await dialogue.bool_dialogue()
                        if dresp.ok:
                            sync_spouses(a_spouses, target.id), sync_spouses(t_spouses, pld.msg.author.id)
                            a_spouses.append({'user_id': target.id, 'time': arrow.utcnow().int_timestamp})
                            t_spouses.append({'user_id': pld.msg.author.id, 'time': arrow.utcnow().int_timestamp})
                            await cmd.db.set_profile(pld.msg.author.id, 'spouses', a_spouses)
                            await cmd.db.set_profile(fake_msg.author.id, 'spouses', t_spouses)
                            congrats_title = f'🎉 Congrats to {author.name} and {target.name}!'
                            response = discord.Embed(color=0x66cc66, title=congrats_title)
                        else:
                            if dresp.timed_out:
                                response = discord.Embed(color=0x696969, title=f'🕙 {target.name} didn\'t respond.')
                            elif dresp.cancelled:
                                response = discord.Embed(color=0xe75a70, title=f'💔 {target.name} rejected you.')
                            else:
                                response = dresp.generic('proposal')
                    else:
                        if author.id in t_spouse_ids:
                            response = error(f'You and {target.name} are already married.')
                        else:
                            response = error(f'You already proposed to {target.name}.')
                else:
                    limited = author if a_limited else target
                    response = discord.Embed(color=0xe75a70, title=f'💔 {limited.name} has too many spouses.')
            else:
                response = discord.Embed(color=0xe75a70, title='💔 Machines aren\'t that advanced yet.')
        else:
            response = discord.Embed(color=0xe75a70, title='💔 You love yourself too much.')
    else:
        response = error('No user targeted.')
    await pld.msg.channel.send(embed=response)
