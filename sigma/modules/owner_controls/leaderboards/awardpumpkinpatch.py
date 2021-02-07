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

from sigma.core.mechanics.resources import SigmaResource
from sigma.core.utilities.generic_responses import GenericResponse


async def awardpumpkinpatch(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    await pld.msg.add_reaction('🎃')
    guild_sums = {}
    guild_counts = {}
    guild_participants = {}
    all_weights = await cmd.db[cmd.db.db_nam].WeightResource.find({}).to_list(None)
    for weight in all_weights:
        resource = SigmaResource(weight)
        if not await cmd.db.is_sabotaged(resource.raw.get('user_id')):
            for guild_key in resource.origins.guilds.keys():
                guild_part = guild_participants.get(guild_key, [])
                guild_part.append({'id': resource.raw.get('user_id'), 'val': resource.origins.guilds.get(guild_key)})
                guild_total = guild_sums.get(guild_key, 0)
                guild_count = guild_counts.get(guild_key, 0)
                guild_total += resource.origins.guilds.get(guild_key)
                guild_count += 1
                guild_sums.update({guild_key: guild_total})
                guild_counts.update({guild_key: guild_count})
                guild_participants.update({guild_key: guild_part})
    guild_sum_list = []
    for gsk in guild_sums.keys():
        guild_sum_list.append({
            'id': int(gsk),
            'val': guild_sums.get(gsk),
            'cnt': guild_counts.get(gsk),
            'avg': guild_sums.get(gsk) / guild_counts.get(gsk)
        })
    guild_sum_list = list(sorted(guild_sum_list, key=lambda x: x.get('avg'), reverse=True))
    award_count = 0
    award_value = 0
    for gsli_x, gsli in enumerate(guild_sum_list):
        guild_multi = 20 - gsli_x if gsli_x < 20 else 0.25
        guild_val = gsli.get('val')
        guild_count = gsli.get('cnt')
        user_list = guild_participants.get(str(gsli.get('id')))
        for user_doc in user_list:
            award_count += 1
            user_id = user_doc.get('id')
            user_val = user_doc.get('val')
            award = int(100000 * guild_multi * (user_val / guild_val) * (guild_count / 1.666))
            award_value += award
            await cmd.db.add_resource(int(user_id), 'currency', award, cmd.name, pld.msg, ranked=False)
    response = GenericResponse(
        f'Awarded {award_count} users a total of {award_value} {cmd.bot.cfg.pref.currency}.'
    ).ok()
    await pld.msg.channel.send(embed=response)
