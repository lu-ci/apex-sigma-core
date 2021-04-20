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
from humanfriendly.tables import format_pretty_table as boop

from sigma.core.utilities.data_processing import user_avatar
from sigma.modules.minigames.nexus.skills.core import SkillCore


async def skills(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    target = pld.msg.mentions[0] if pld.msg.mentions else pld.msg.author
    sc = SkillCore.instance()
    lines = []
    headers = ['Name', 'Pts.', 'Lv.', 'Prog.']
    points = 0
    for skill in sc.skills:
        si = await skill.load(cmd.db, target.id)
        points += si.points
        level = si.level()
        upper = skill.total_needed(level + 1) if level != skill.max_level else si.points
        if upper > int(upper):
            upper = int(upper) + 1
        progress = int(si.progress() * 100)
        lines.append([
            skill.name.title(),
            f'{si.points}/{upper}',
            f'{level}/{skill.max_level}',
            f'{progress}%'
        ])
    response = discord.Embed(color=0xdd_2e_44, title=f'💪 Skills with a total of {points} points.')
    response.set_author(name=f'{target.name}\'s Skills', icon_url=user_avatar(target))
    response.description = f'```hs\n{boop(lines, headers)}\n```'
    await pld.msg.channel.send(embed=response)
