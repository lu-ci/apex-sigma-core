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

from sigma.core.utilities.dialogue_controls import bool_dialogue
from sigma.core.utilities.generic_responses import error, denied
from sigma.modules.utilities.misc.other.event.spooktober.mech.util.enchantment import get_curse_controller
from sigma.modules.utilities.misc.other.event.spooktober.mech.util.enchantment import get_enchantment_controller


async def enchant(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    price = 5
    target = pld.msg.mentions[0] if pld.msg.mentions else None
    if target:
        if not target.bot:
            if target.id != pld.msg.author.id:
                candy = await cmd.db.get_resource(pld.msg.author.id, 'sweets')
                if candy.current >= price:
                    curc = get_curse_controller(cmd.db)
                    cursed = await curc.is_cursed(target.id)
                    if not cursed:
                        encc = get_enchantment_controller(cmd.db)
                        can_enchant = await encc.can_enchant(target.id)
                        if can_enchant:
                            author_can_enchant = await encc.can_author_enchant(pld.msg.author.id, target.id)
                            if author_can_enchant:
                                question_text = f'❔ Enchant {target.display_name} for **{price} Sweets** ?'
                                question = discord.Embed(color=0xf9f9f9, title=question_text)
                                success, timeout = await bool_dialogue(cmd.bot, pld.msg, question)
                                if success:
                                    text = f'💠 You have enchanted {target.display_name} for 2 hours.'
                                    response = discord.Embed(color=0x55acee, title=text)
                                    await encc.add_enchanter(pld.msg.author.id, target.id)
                                    await cmd.db.del_resource(pld.msg.author.id, 'sweets', price, cmd.name, pld.msg)
                                else:
                                    if timeout:
                                        response_text = f'🕙 You didn\'t respond in time.'
                                        response = discord.Embed(color=0x696969, title=response_text)

                                    else:
                                        response_text = f'❌ Enchantment canceled.'
                                        response = discord.Embed(color=0xBE1931, title=response_text)
                            else:
                                response = denied(f'You already enchanted {target.display_name}.')
                                ench_timer = await encc.author_enchantment_expires(pld.msg.author.id, target.id, True)
                                response.set_footer(text=f'Your enchantment expires in {ench_timer}.')
                        else:
                            response = denied(f'{target.display_name} already has two enchantments.')
                            ench_timer = await encc.shortest_enchantment_expires(target.id, True)
                            response.set_footer(text=f'The shortest enchantment expires in {ench_timer}.')
                    else:
                        text = f'☠ {target.display_name} is cursed and can\'t be enchanted right now.'
                        response = discord.Embed(color=0x361683, title=text)
                        curse_timer = await curc.get_cursed_time(target.id, True)
                        response.set_footer(text=f'Their curse expires in: {curse_timer}')
                else:
                    response = error(f'You don\'t have enough sweets: {candy.current}/{price}.')
            else:
                response = error('You can\'t enchant yourself.')
        else:
            response = error('No, the candy dust just makes bots sneeze.')
    else:
        response = error('No target given.')
    await pld.msg.channel.send(embed=response)
