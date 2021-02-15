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
from sigma.core.utilities.generic_responses import GenericResponse


async def send_divorce(author, target):
    """
    :type author: discord.Member
    :type target: discord.Member
    """
    divorce_embed = discord.Embed(color=0xe75a70, title=f'💔 {author.name} has divorced you...')
    try:
        await target.send(embed=divorce_embed)
    except (discord.Forbidden, discord.HTTPException):
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
                time_diff = arrow.utcnow().int_timestamp - marry_stamp
                div_cost = int(time_diff * 0.004)
                currency = cmd.bot.cfg.pref.currency
                if is_id:
                    option_message = discord.Embed(color=0xf9f9f9, title='❔ How do you want to do this?')
                    option_message.description = f'\n**1.** Force a divorce. **({div_cost} {currency})**'
                    option_message.description += '\n**2. Cancel.**'
                    start, end = 1, 2
                else:
                    option_message = discord.Embed(color=0xf9f9f9, title='❔ How do you want to do this?')
                    option_message.description = f'**1.** Ask for a mutual divorce. **(0 {currency})**'
                    option_message.description += f'\n**2.** Force a divorce. **({div_cost} {currency})**'
                    option_message.description += '\n**3. Cancel.**'
                    start, end = 1, 3
                option_dialogue = DialogueCore(cmd.bot, pld.msg, option_message)
                option_dresp = await option_dialogue.int_dialogue(start, end)
                if not option_dresp.timed_out:
                    if option_dresp.value is not (3 if not is_id else 2):
                        fault = None
                        can_proceed = False
                        ask_mutual = option_dresp.value == 1 and not is_id
                        if ask_mutual:
                            div_cost = 0
                            hacked_message = copy.copy(pld.msg)
                            hacked_message.author = target
                            question_text = f'❔ {target.name}, do you agree to a mutual divorce?'
                            question = discord.Embed(color=0xf9f9f9, title=question_text)
                            dialogue = DialogueCore(cmd.bot, hacked_message, question)
                            dresp = await dialogue.bool_dialogue()
                            if not dresp.timed_out:
                                if dresp.ok:
                                    can_proceed = True
                                elif dresp.cancelled:
                                    fault = 'rejected the divorce'
                                else:
                                    fault = dresp.generic('mutual divorce')
                            else:
                                fault = 'took too long to answer'
                        else:
                            can_proceed = True
                        if can_proceed:
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
                                    await send_divorce(pld.msg.author, target)
                                await cmd.db.del_resource(pld.msg.author.id, 'currency', div_cost, cmd.name, pld.msg)
                            else:
                                response = GenericResponse(
                                    f'You don\'t have {div_cost} {currency} to get a divorce.'
                                ).error()
                        else:
                            if isinstance(fault, discord.Embed):
                                response = fault
                            else:
                                response = GenericResponse(f'Couldn\'t proceed because {target.name} {fault}.').error()
                    else:
                        response = GenericResponse('Divorce withdrawn.').error()
                else:
                    response = discord.Embed(color=0x696969, title='🕙 Sorry, you timed out.')
            else:
                if is_id:
                    response = GenericResponse(f'You aren\'t married to {target}.').error()
                else:
                    response = GenericResponse(f'You aren\'t married to {target.name}.').error()
        else:
            response = GenericResponse('Can\'t divorce yourself.').error()
    else:
        response = GenericResponse('No user targeted.').error()
    await pld.msg.channel.send(embed=response)
