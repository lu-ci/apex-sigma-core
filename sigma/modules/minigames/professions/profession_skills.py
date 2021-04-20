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

from sigma.modules.minigames.nexus.skills.core import Skill, SkillCore


class ProfessionSkill(Skill):
    def __init__(self, name: str):
        super().__init__(name, 3.69, 0.015, 50)

    def effect(self) -> object:
        return lambda pts: 60 - (1 + (self.level(pts) ** 2) * 0.015)


async def profession_skills(_ev):
    """
    :param _ev: The event object referenced in the event.
    :type _ev: sigma.core.mechanics.event.SigmaEvent
    """
    professions = ['fishing', 'hunting', 'foraging']
    sc = SkillCore.instance()
    for profession in professions:
        skill = ProfessionSkill(profession)
        sc.add_skill(skill)
