import asyncio

import discord

from .nodes.upgrades import upgrade_list

ongoing = []


async def buyupgrade(cmd, message, args):
    if message.author.id not in ongoing:
        ongoing.append(message.author.id)
        upgrade_file = await cmd.db[cmd.db.db_cfg.database].Upgrades.find_one({'UserID': message.author.id})
        if upgrade_file is None:
            await cmd.db[cmd.db.db_cfg.database].Upgrades.insert_one({'UserID': message.author.id})
            upgrade_file = {}
        upgrade_text = ''
        upgrade_index = 0
        for upgrade in upgrade_list:
            upgrade_index += 1
            upgrade_id = upgrade['id']
            if upgrade_id in upgrade_file:
                upgrade_level = upgrade_file[upgrade_id]
            else:
                upgrade_level = 0
            base_price = upgrade['cost']
            if upgrade_level == 0:
                upgrade_price = base_price
            else:
                price_mod = int(base_price * upgrade_level * (1.20 + (0.115 * upgrade_level)))
                upgrade_price = price_mod + (price_mod // 2)
            currency = cmd.bot.cfg.pref.currency
            next_upgrade = upgrade_level + 1
            upgrade_text += f'\n**{upgrade_index}**: Level {next_upgrade} {upgrade["name"]}'
            upgrade_text += f' - {upgrade_price} {currency}'
            upgrade_text += f'\n > {upgrade["desc"]}'
        upgrade_list_embed = discord.Embed(color=0xF9F9F9, title='🛍 Sigma\'s Profession Upgrade Shop')
        upgrade_list_embed.description = upgrade_text
        upgrade_list_embed.set_footer(text='Please input the number of the upgrade you want.')
        shop_listing = await message.channel.send(embed=upgrade_list_embed)

        def check_answer(msg):
            if message.author.id == msg.author.id:
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
                current_kud = await cmd.db.get_currency(message.author, message.guild)
                current_kud = current_kud['current']
                upgrade_id = upgrade['id']
                if upgrade_id in upgrade_file:
                    upgrade_level = upgrade_file[upgrade_id]
                else:
                    upgrade_level = 0
                base_price = upgrade['cost']
                if upgrade_level == 0:
                    upgrade_price = base_price
                else:
                    price_mod = int(base_price * upgrade_level * (1.20 + (0.115 * upgrade_level)))
                    upgrade_price = price_mod + (price_mod // 2)
                if current_kud >= upgrade_price:
                    new_upgrade_level = upgrade_level + 1
                    upgrade_data = {'$set': {upgrade_id: new_upgrade_level}}
                    await cmd.db[cmd.db.db_cfg.database].Upgrades.update_one({'UserID': message.author.id},
                                                                             upgrade_data)
                    await cmd.db.rmv_currency(message.author, upgrade_price)
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
            await message.channel.send(embed=response)
        except asyncio.TimeoutError:
            timeout_title = f'🕙 Sorry, you timed out, feel free to open the shop again.'
            timeout_embed = discord.Embed(color=0x696969, title=timeout_title)
            await message.channel.send(embed=timeout_embed)
        if message.author.id in ongoing:
            ongoing.remove(message.author.id)
    else:
        ongoing_response = discord.Embed(color=0xBE1931, title='❗ You already have a shop open.')
        await message.channel.send(embed=ongoing_response)
