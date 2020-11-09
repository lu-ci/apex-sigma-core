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
import humanfriendly
from pympler import asizeof

from sigma.core.utilities.generic_responses import info
from sigma.modules.core_functions.chatter_core.chatter_core_init import chatter_core
from sigma.modules.minigames.racing.nodes.race_storage import races
from sigma.modules.minigames.utils.ongoing.ongoing import stats as ongoing_stats


async def memorystats(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    start = arrow.utcnow().float_timestamp
    response = info("Memory Statistics")
    og_keys, og_ids, og_size = ongoing_stats()
    og_time = round(arrow.utcnow().float_timestamp - start, 3)
    response.add_field(
        name='Ongoing',
        value=f"Keys: {og_keys}\nIdentifiers: {og_ids}\nSize: {og_size}\nTime: {og_time}s"
    )
    cache_stats = await cmd.db.cache.format_stats()
    cache_time = round(arrow.utcnow().float_timestamp - start, 3)
    response.add_field(
        name='Cacher',
        value=f"{cache_stats}\nTime: {cache_time}s"
    )
    chatter = humanfriendly.format_size(asizeof.asizeof(chatter_core), binary=True)
    race_size = humanfriendly.format_size(asizeof.asizeof(races), binary=True)
    cd_scaling = humanfriendly.format_size(asizeof.asizeof(cmd.bot.cool_down.scaling), binary=True)
    spc_time = round(arrow.utcnow().float_timestamp - start, 3)
    response.add_field(
        name='Specific',
        value=f"Chatter: {chatter}\nRaces: {race_size}\nCD Scaling: {cd_scaling}\nTime: {spc_time}s"
    )
    await pld.msg.channel.send(embed=response)
