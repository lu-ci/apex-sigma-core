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

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import error, ok
from sigma.modules.fun.family.models.human import AdoptableHuman


async def disown(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    target = pld.msg.mentions[0] if pld.msg.mentions else None
    if target is not None:
        disowner = AdoptableHuman(cmd.db, pld.msg.author.id)
        await disowner.load()
        if not disowner.exists:
            await disowner.new(pld.msg.author)
        else:
            disowner.update_name(pld.msg.author.name)
        disownee = AdoptableHuman(cmd.db, target.id)
        await disownee.load()
        if not disownee.exists:
            await disownee.new(target)
        else:
            disownee.update_name(target.name)
        if disowner.id in [par.id for par in disownee.parents]:
            update = True
            disowner.children = [dcld for dcld in disowner.children if dcld.id != disownee.id]
            disownee.parents = [dpar for dpar in disownee.parents if dpar.id != disowner.id]
            response = ok(f'{target.name} is no longer your child.')
        elif disowner.id in [cld.id for cld in disownee.children]:
            update = True
            disowner.parents = [dpar for dpar in disowner.parents if dpar.id != disownee.id]
            disownee.children = [dcld for dcld in disownee.children if dcld.id != disowner.id]
            response = ok(f'{target.name} is no longer your parent.')
        else:
            update = False
            response = error(f'{target.name} is not part of your immediate family.')
        [await human.save() for human in [disowner, disownee] if update]
    else:
        response = error('No user targeted.')
    await pld.msg.channel.send(embed=response)
