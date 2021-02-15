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


async def sell_item_ids(db, user, items):
    """
    :type db:
    :type user:
    :type items:
    """
    inv = await db.get_inventory(user.id)
    for item in items:
        for inv_item in inv:
            if inv_item['item_id'] == item:
                inv.remove(inv_item)
    await db.update_inventory(user.id, inv)


async def filtersell(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    item_core = await get_item_core(cmd.db)
    if pld.args:
        full_qry = ' '.join(pld.args)
        arguments = full_qry.split(':')
        if len(arguments) >= 2:
            mode = arguments[0].lower()
            lookup = ' '.join(arguments[1:])
            inv = await cmd.db.get_inventory(pld.msg.author.id)
            if inv:
                value = 0
                count = 0
                if mode == 'name':
                    attribute = 'name'
                elif mode == 'type':
                    attribute = 'type'
                elif mode == 'rarity' or mode == 'quality':
                    attribute = 'rarity_name'
                else:
                    attribute = None
                if attribute:
                    sell_id_list = []
                    for item in inv:
                        item_ob_id = item_core.get_item_by_file_id(item['item_file_id'])
                        item_attribute = getattr(item_ob_id, attribute)
                        if item_attribute.lower() == lookup.lower():
                            value += item_ob_id.value
                            count += 1
                            sell_id_list.append(item['item_id'])
                    if sell_id_list:
                        ender = 's' if count > 1 else ''
                        currency = cmd.bot.cfg.pref.currency
                        question = f'❔ Are you sure you want to sell {count} item{ender} worth {value} {currency}?'
                        quesbed = discord.Embed(color=0xF9F9F9, title=question)
                        dialogue = DialogueCore(cmd.bot, pld.msg, quesbed)
                        dresp = await dialogue.bool_dialogue()
                        if dresp.ok:
                            await sell_item_ids(cmd.db, pld.msg.author, sell_id_list)
                            await cmd.db.add_resource(pld.msg.author.id, 'currency', value, cmd.name, pld.msg)
                            response = discord.Embed(color=0xc6e4b5)
                            response.title = f'💶 You sold {count} item{ender} for {value} {currency}.'
                        else:
                            response = dresp.generic(f'item sale by {mode}')
                    else:
                        response = GenericResponse('No items with the selected criteria were found.').not_found()
                else:
                    response = GenericResponse('Invalid arguments.').error()
            else:
                response = discord.Embed(color=0xc6e4b5, title='💸 Your inventory is empty...')
        else:
            response = GenericResponse('Not enough arguments.').error()
    else:
        response = GenericResponse('Nothing inputted.').error()
    response.set_author(name=pld.msg.author.display_name, icon_url=user_avatar(pld.msg.author))
    await pld.msg.channel.send(embed=response)
