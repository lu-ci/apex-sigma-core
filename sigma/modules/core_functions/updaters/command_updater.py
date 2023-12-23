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

import asyncio

command_clock_running = False


async def command_updater(ev):
    """
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    global command_clock_running
    if not command_clock_running:
        if ev.bot.cfg.dsc.shards is None or 0 in ev.bot.cfg.dsc.shards:
            ev.bot.loop.create_task(command_updater_cycler(ev))
        command_clock_running = True


async def gen_cmd_cache_data(cmd, mdl_coll):
    """
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :type mdl_coll: motor.motor_asyncio.AsyncIOMotorCollection
    :rtype: dict
    """
    mdl_doc = await mdl_coll.find_one({'name': cmd.category})
    cmd_data = {
        "desc": cmd.desc,
        "alts": cmd.alts,
        "name": cmd.name,
        "usage": cmd.usage,
        "nsfw": cmd.nsfw,
        "partner": cmd.partner,
        "admin": cmd.owner,
        "category_id": mdl_doc.get('_id')
    }
    return cmd_data


async def command_updater_cycler(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    module_coll = ev.db.col.ModuleCache
    command_coll = ev.db.col.CommandCache
    await module_coll.drop()
    await command_coll.drop()
    while True:
        if ev.bot.is_ready():
            for module in ev.bot.modules.categories:
                await module_coll.insert_one({'name': module})
            for command in ev.bot.modules.commands:
                command = ev.bot.modules.commands.get(command)
                command_data = await gen_cmd_cache_data(command, module_coll)
                await command_coll.insert_one(command_data)
        await asyncio.sleep(3600)
