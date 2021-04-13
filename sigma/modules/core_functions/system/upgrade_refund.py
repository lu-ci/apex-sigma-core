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
from sigma.modules.minigames.professions.buyupgrade import get_price
from sigma.modules.minigames.professions.nodes.upgrade_params import upgrade_list


async def upgrade_refund(ev, force=False):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :type force: bool
    """
    refunded = 0
    upgrade_costs = {}
    for upgrade in upgrade_list:
        upgrade_costs.update({upgrade['id']: upgrade['cost']})
    if ev.bot.cfg.dsc.shards is None or 0 in ev.bot.cfg.dsc.shards:
        profiles = await ev.db[ev.db.db_nam].Profiles.find()
        async for profile in profiles:
            amount = 0
            upgrades = profile.get('upgrades') or {}
            if upgrades:
                for upg in upgrades.keys():
                    level = upgrades.get(upg)
                    if level:
                        base = upgrade_costs.get(upg)
                        for lv in range(0, level + 1):
                            amount += get_price(base, lv)
            uid = profile.get('user_id')
            await ev.db.add_resource(uid, 'currency', amount, ev.name)
            await ev.db.set_profile(uid, 'upgrades', {})
            refunded += 1
    if refunded:
        ev.log.info(f'Refunded {refunded} upgrade sets.')
