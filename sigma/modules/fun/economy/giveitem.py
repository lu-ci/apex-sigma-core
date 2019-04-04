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

from sigma.core.utilities.generic_responses import error, not_found, ok
from sigma.modules.minigames.professions.nodes.item_core import get_item_core


async def giveitem(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    item_core = await get_item_core(cmd.db)
    if len(pld.args) > 1:
        if pld.msg.mentions:
            target = pld.msg.mentions[0]
            lookup = ' '.join(pld.args[1:])
            obj_item = item_core.get_item_by_name(lookup)
            if obj_item:
                inv_item = await cmd.db.get_inventory_item(pld.msg.author.id, obj_item.file_id)
                if inv_item:
                    upgrade_file = await cmd.db.get_profile(target.id, 'upgrades') or {}
                    inv = await cmd.db.get_inventory(target.id)
                    storage = upgrade_file.get('storage', 0)
                    inv_limit = 64 + (8 * storage)
                    author_sab = await cmd.db.is_sabotaged(pld.msg.author.id)
                    target_sab = await cmd.db.is_sabotaged(target.id)
                    if len(inv) < inv_limit:
                        if not author_sab and not target_sab:
                            await cmd.db.del_from_inventory(pld.msg.author.id, inv_item.get('item_id'))
                            inv_item.update({'transferred': True})
                            await cmd.db.add_to_inventory(target.id, inv_item)
                            await cmd.db.add_resource(target.id, 'items', 1, cmd.name, pld.msg, True)
                            response = ok(f'Transferred {obj_item.name} to {target.display_name}.')
                            response.set_footer(text=f'Item ID: {inv_item.get("item_id")}')
                        else:
                            response = error('Transfer declined by Lucia\'s Guard.')
                    else:
                        response = error(f'{target.name}\'s inventory is full.')
                else:
                    response = not_found(f'No {obj_item.name} found in your inventory.')
            else:
                response = not_found('No such item exists.')
        else:
            response = error('No user targeted.')
    else:
        response = error('Not enough arguments.')
    await pld.msg.channel.send(embed=response)
