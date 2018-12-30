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

import asyncio

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.modules.minigames.warmachines.mech.machine import SigmaMachine

price = 0


async def warmachinenew(cmd: SigmaCommand, pld: CommandPayload):
    confirm_desc = f'Building a machine costs **{price} sumarum**, do you want to continue?'
    confirm_embed = discord.Embed(color=0x8899a6, title=f'🔧 Are you sure, {pld.msg.author.name}?')
    confirm_embed.description = confirm_desc
    confirmation = await pld.msg.channel.send(embed=confirm_embed)
    await confirmation.add_reaction('✅')
    await confirmation.add_reaction('❌')

    def check_emote(reac, usr):
        return usr.id == pld.msg.author.id and str(reac.emoji) in ['✅', '❌']

    try:
        ae, au = await cmd.bot.wait_for('reaction_add', timeout=60, check=check_emote)
        try:
            await confirmation.delete()
        except discord.NotFound:
            pass
        if ae.emoji == '✅':
            canceled = False
        else:
            canceled = True
    except asyncio.TimeoutError:
        canceled = True
    if not canceled:
        sumarum = await cmd.db.get_resource(pld.msg.author.id, 'sumarum')
        if sumarum.current >= price:
            await cmd.db.del_resource(pld.msg.author.id, 'sumarum', price, cmd.name, pld.msg)
            prefix = cmd.db.get_prefix(pld.settings)
            machine = SigmaMachine(cmd.db, pld.msg.author, SigmaMachine.new())
            await machine.update()
            response = discord.Embed(color=0x8899a6, title=f'🔧 {machine.product_name} constructed.')
            response.set_footer(text=f'Use "{prefix}wminspect {machine.id}" to see its specifications.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Not enough sumarum.')
    else:
        response = discord.Embed(color=0xBE1931, title='❌ Construction canceled.')
    await pld.msg.channel.send(embed=response)
