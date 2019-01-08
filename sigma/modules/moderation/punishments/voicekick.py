# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2018  Lucia's Cipher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import denied
from sigma.core.utilities.permission_processing import hierarchy_permit


async def voicekick(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.permissions_in(pld.msg.channel).kick_members:
        if pld.msg.mentions:
            target = pld.msg.mentions[0]
            if cmd.bot.user.id != target.id:
                if pld.msg.author.id != target.id:
                    above_hier = hierarchy_permit(pld.msg.author, target)
                    is_admin = pld.msg.author.permissions_in(pld.msg.channel).administrator
                    if above_hier or is_admin:
                        above_me = hierarchy_permit(pld.msg.guild.me, target)
                        if above_me:
                            if target.voice:
                                tvc = target.voice.channel
                                tempvc = discord.utils.find(lambda x: x.name == 'Kick Hall', pld.msg.guild.channels)
                                if not tempvc:
                                    tempvc = await pld.msg.guild.create_voice_channel('Kick Hall')
                                await target.move_to(tempvc)
                                await tempvc.delete()
                                remove_title = f'👢 {target.name} has been removed from {tvc.name}.'
                                response = discord.Embed(color=0xc1694f, title=remove_title)
                            else:
                                not_in_voice = f'❗ {target.name} is not in a voice channel.'
                                response = discord.Embed(color=0xBE1931, title=not_in_voice)
                        else:
                            response = discord.Embed(color=0xBE1931, title='⛔ Target is above my highest role.')
                    else:
                        response = discord.Embed(color=0xBE1931, title='⛔ Can\'t kick someone equal or above you.')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ You can\'t kick yourself.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ I can\'t kick myself.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ No user targeted.')
    else:
        response = denied('Kick permissions')
    await pld.msg.channel.send(embed=response)
