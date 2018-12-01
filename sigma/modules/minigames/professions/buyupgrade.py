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
from sigma.modules.minigames.professions.nodes.upgrade_params import upgrade_list

ongoing = []


def get_price_mod(base_price, upgrade_level):
    return int(base_price * upgrade_level * (1.10 + (0.075 * upgrade_level)))


async def buyupgrade(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.id not in ongoing:
        ongoing.append(pld.msg.author.id)
        upgrade_file = await cmd.bot.db.get_profile(pld.msg.author.id, 'upgrades') or {}
        upgrade_text = ''
        upgrade_index = 0
        for upgrade in upgrade_list:
            upgrade_index += 1
            upgrade_id = upgrade.get('id')
            upgrade_level = upgrade_file.get(upgrade_id, 0)
            base_price = upgrade.get('cost')
            if upgrade_level == 0:
                upgrade_price = base_price
            else:
                price_mod = get_price_mod(base_price, upgrade_level)
                upgrade_price = price_mod + (price_mod // 2)
            currency = cmd.bot.cfg.pref.currency
            next_upgrade = upgrade_level + 1
            upgrade_text += f'\n**{upgrade_index}**: Level {next_upgrade} {upgrade["name"]}'
            upgrade_text += f' - {upgrade_price} {currency}'
            upgrade_text += f'\n > {upgrade["desc"]}'
        upgrade_list_embed = discord.Embed(color=0xF9F9F9, title='🛍 Profession Upgrade Shop')
        upgrade_list_embed.description = upgrade_text
        upgrade_list_embed.set_footer(text='Please input the number of the upgrade you want.')
        shop_listing = await pld.msg.channel.send(embed=upgrade_list_embed)

        def check_answer(msg):
            if pld.msg.author.id == msg.author.id:
                if msg.content.lower() == 'cancel':
                    correct = True
                else:
                    try:
                        an_num = int(msg.content)
                        if 0 < an_num <= len(upgrade_list):
                            correct = True
                        else:
                            correct = False
                    except ValueError:
                        correct = False
            else:
                correct = False
            return correct

        try:
            answer_message = await cmd.bot.wait_for('message', check=check_answer, timeout=30)
            if answer_message.content.lower() != 'cancel':
                upgrade_number = int(answer_message.content) - 1
                upgrade = upgrade_list[upgrade_number]
                current_kud = await cmd.db.get_resource(pld.msg.author.id, 'currency')
                current_kud = current_kud.current
                upgrade_id = upgrade['id']
                if upgrade_id in upgrade_file:
                    upgrade_level = upgrade_file[upgrade_id]
                else:
                    upgrade_level = 0
                base_price = upgrade['cost']
                if upgrade_level == 0:
                    upgrade_price = base_price
                else:
                    price_mod = get_price_mod(base_price, upgrade_level)
                    upgrade_price = price_mod + (price_mod // 2)
                if current_kud >= upgrade_price:
                    new_upgrade_level = upgrade_level + 1
                    upgrade_file.update({upgrade_id: new_upgrade_level})
                    await cmd.db.set_profile(pld.msg.author.id, 'upgrades', upgrade_file)
                    await cmd.db.del_resource(pld.msg.author.id, 'currency', upgrade_price, cmd.name, pld.msg)
                    upgrade_title = f'✅ Upgraded your {upgrade["name"]} to Level {new_upgrade_level}.'
                    response = discord.Embed(color=0x77B255, title=upgrade_title)
                else:
                    response = discord.Embed(color=0xa7d28b, title=f'💸 You don\'t have enough {currency}.')
            else:
                response = discord.Embed(color=0xF9F9F9, title='🛍 Shop exited.')
            try:
                await shop_listing.delete()
            except discord.NotFound:
                pass
            await pld.msg.channel.send(embed=response)
        except asyncio.TimeoutError:
            timeout_title = f'🕙 Sorry, you timed out, feel free to open the shop again.'
            timeout_embed = discord.Embed(color=0x696969, title=timeout_title)
            await pld.msg.channel.send(embed=timeout_embed)
        if pld.msg.author.id in ongoing:
            ongoing.remove(pld.msg.author.id)
    else:
        ongoing_response = discord.Embed(color=0xBE1931, title='❗ You already have a shop open.')
        await pld.msg.channel.send(embed=ongoing_response)
