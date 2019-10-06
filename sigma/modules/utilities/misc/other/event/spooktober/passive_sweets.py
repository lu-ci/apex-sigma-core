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

from sigma.modules.utilities.misc.other.event.spooktober.mech.resources.sweets import SweetsController
from sigma.modules.utilities.misc.other.event.spooktober.mech.resources.vigor import get_vigor_controller


async def passive_sweets(ev, pld):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :param pld: The event payload data to process.
    :type pld: sigma.core.mechanics.payload.MessagePayload
    """
    if pld.msg.content:
        if not pld.msg.content.startswith(ev.bot.cfg.pref.prefix):
            if pld.msg.guild:
                humans = len([m for m in pld.msg.guild.members if not m.bot])
                if humans >= 5:
                    cd_key = f'{ev.name}_{pld.msg.guild.id}'
                    trigger_roll = secrets.randbelow(666)
                    if trigger_roll < 10:
                        if not await ev.bot.cool_down.on_cooldown(cd_key, pld.msg.author):
                            vc = get_vigor_controller(ev.db)
                            cooldown = await vc.get_cooldown(pld.msg.author.id, 60)
                            await ev.bot.cool_down.set_cooldown(cd_key, pld.msg.author, cooldown)
                            bonus = secrets.randbelow(666) == 0
                            value = 6 if bonus else 1
                            await SweetsController.add_sweets(ev.db, pld.msg, value, ev.name)
