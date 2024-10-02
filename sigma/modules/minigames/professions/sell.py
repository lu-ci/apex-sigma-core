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

import discord

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.dialogue_controls import DialogueCore
from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.minigames.professions.nodes.item_core import get_item_core
from sigma.modules.minigames.utils.ongoing.ongoing import Ongoing


async def sell(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if Ongoing.is_ongoing(cmd.name, pld.msg.author.id):
        return
    Ongoing.set_ongoing(cmd.name, pld.msg.author.id)
    item_core = await get_item_core(cmd.db)
    currency = cmd.bot.cfg.pref.currency
    if pld.args:
        inv = await cmd.db.get_inventory(pld.msg.author.id)
        if inv:
            lookup = ' '.join(pld.args)
            if lookup.lower() == 'all':
                ender = 's' if len(inv) > 1 else ''
                worth = sum([item_core.get_item_by_file_id(ient['item_file_id']).value for ient in inv])
                question = f'❔ Are you sure you want to sell {len(inv)} item{ender} worth {worth} {currency}?'
                quesbed = discord.Embed(color=0xF9F9F9, title=question)
                dialogue = DialogueCore(cmd.bot, pld.msg, quesbed)
                dresp = await dialogue.bool_dialogue()
                if dresp.ok:
                    value = 0
                    count = 0
                    for invitem in inv.copy():
                        item_ob_id = item_core.get_item_by_file_id(invitem['item_file_id'])
                        value += item_ob_id.value
                        count += 1
                        await cmd.db.del_from_inventory(pld.msg.author.id, invitem['item_id'])
                    await cmd.db.add_resource(pld.msg.author.id, 'currency', value, cmd.name, pld.msg)
                    response = discord.Embed(color=0xc6e4b5)
                    response.title = f'💶 You sold {count} item{ender} for {value} {currency}.'
                else:
                    response = dresp.generic('item sale')
            elif lookup.lower() == 'duplicates':
                value = 0
                count = 0
                existing_ids = []
                for invitem in inv.copy():
                    file_id = invitem['item_file_id']
                    if file_id in existing_ids:
                        item_ob_id = item_core.get_item_by_file_id(file_id)
                        value += item_ob_id.value
                        count += 1
                        await cmd.db.del_from_inventory(pld.msg.author.id, invitem['item_id'])
                    else:
                        existing_ids.append(file_id)
                await cmd.db.add_resource(pld.msg.author.id, 'currency', value, cmd.name, pld.msg)
                ender = 's' if count > 1 else ''
                response = discord.Embed(color=0xc6e4b5)
                response.title = f'💶 You sold {count} duplicate{ender} for {value} {currency}.'
            else:
                request_count = 1
                if len(pld.args) > 1:
                    if pld.args[0].isdigit():
                        request_count = int(pld.args[0])
                        lookup = ' '.join(pld.args[1:])
                item_o = item_core.get_item_by_name(lookup)
                count = 0
                value = 0
                had_item = False
                if item_o:
                    for _ in range(request_count):
                        item = await cmd.db.get_inventory_item(pld.msg.author.id, item_o.file_id)
                        had_item = True
                        if item:
                            if item_o.value:
                                value += item_o.value
                                count += 1
                                await cmd.db.del_from_inventory(pld.msg.author.id, item['item_id'])
                            else:
                                break
                        else:
                            break
                if count > 0:
                    await cmd.db.add_resource(pld.msg.author.id, 'currency', value, cmd.name, pld.msg)
                    ender = 's' if count > 1 else ''
                    response = discord.Embed(color=0xc6e4b5)
                    response.title = f'💶 You sold {count} {item_o.name}{ender} for {value} {currency}.'
                else:
                    if not lookup.isdigit():
                        if had_item:
                            response = GenericResponse('We stopped your sale because of a calculation error.').error()
                            response.description = 'Sometimes, the resulting sale price ends up being 0. '
                            response.description += 'Try checking the item with the `inspect` command first '
                            response.description += 'and then just try again.'
                        else:
                            response = GenericResponse(f'I didn\'t find any {lookup} in your inventory.').not_found()
                    else:
                        response = GenericResponse(f'Sell {lookup} of what?').not_found()
        else:
            response = discord.Embed(color=0xc6e4b5, title='💸 Your inventory is empty...')
    else:
        response = GenericResponse('Nothing inputted.').error()
    if Ongoing.is_ongoing(cmd.name, pld.msg.author.id):
        Ongoing.del_ongoing(cmd.name, pld.msg.author.id)
    response.set_author(name=pld.msg.author.display_name, icon_url=user_avatar(pld.msg.author))
    await pld.msg.channel.send(embed=response)
