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
from sigma.core.mechanics.database import Database
from sigma.modules.minigames.warmachines.mech.machine import SigmaMachine

price = 450
resource_names = ['metal', 'biomass', 'ammunition', 'sumarum', 'currency']


async def check_resources(db: Database, uid: int):
    missing = []
    for res in resource_names:
        user_res = await db.get_resource(uid, res)
        if user_res.current < price:
            missing.append(res)
    return missing


async def warmachinenew(cmd: SigmaCommand, pld: CommandPayload):
    res_list = '{", ".join(resource_names)}'.replace('currency', cmd.bot.cfg.pref.currency.lower())
    confirm_desc = f'Building a machine costs **{price}** of **{res_list}** each, do you want to continue?'
    confirm_embed = discord.Embed(color=0x8899a6, title=f'🔧 Are you sure, {message.author.name}?')
    confirm_embed.description = confirm_desc
    confirmation = await message.channel.send(embed=confirm_embed)
    await confirmation.add_reaction('✅')
    await confirmation.add_reaction('❌')

    def check_emote(reac, usr):
        return usr.id == message.author.id and str(reac.emoji) in ['✅', '❌']

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
        missing = await check_resources(cmd.db, message.author.id)
        if not missing:
            for res in resource_names:
                await cmd.db.del_resource(message.author.id, res, price, cmd.name, message)
            prefix = await cmd.db.get_prefix(message)
            machine = SigmaMachine(cmd.db, message.author, SigmaMachine.new())
            await machine.update()
            response = discord.Embed(color=0x8899a6, title=f'🔧 {machine.product_name} constructed.')
            response.set_footer(text=f'Use "{prefix}wminspect {machine.id}" to see its specifications.')
        else:
            missing_list = f'{", ".join(missing)}'.replace('currency', cmd.bot.cfg.pref.currency.lower())
            response = discord.Embed(color=0xBE1931, title=f'❗ Not enough {missing_list}.')
    else:
        response = discord.Embed(color=0xBE1931, title=f'❌ Construction canceled.')
    await message.channel.send(embed=response)
