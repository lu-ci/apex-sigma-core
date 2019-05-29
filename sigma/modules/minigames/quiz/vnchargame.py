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

import asyncio
import secrets

import aiohttp
import discord
from lxml import html

from sigma.core.utilities.generic_responses import error
from sigma.modules.minigames.quiz.mech.utils import scramble
from sigma.modules.minigames.utils.ongoing.ongoing import is_ongoing, set_ongoing, del_ongoing

streaks = {}


async def vnchargame(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if not is_ongoing(cmd.name, pld.msg.channel.id):
        try:
            set_ongoing(cmd.name, pld.msg.channel.id)
            vndb_icon = 'https://i.imgur.com/YrK5tQF.png'
            wait_embed = discord.Embed(color=0x1d439b)
            wait_embed.set_author(name='Hunting for a good specimen...', icon_url=vndb_icon)
            working_response = await pld.msg.channel.send(embed=wait_embed)
            if pld.args:
                if pld.args[0].lower() == 'hint':
                    hint = True
                else:
                    hint = False
            else:
                hint = False
            vn_url_list = []
            vn_top_list_url = f'https://vndb.org/v/all?q=;fil=tagspoil-0;rfil=;o=d;s=pop;p=1'
            async with aiohttp.ClientSession() as session:
                async with session.get(vn_top_list_url) as vn_top_list_session:
                    vn_top_list_html = await vn_top_list_session.text()
            vn_top_list_data = html.fromstring(vn_top_list_html)
            list_items = vn_top_list_data.cssselect('.tc1')
            for list_item in list_items:
                if 'href' in list_item[0].attrib:
                    vn_url = list_item[0].attrib['href']
                    if vn_url.startswith('/v') and not vn_url.startswith('/v/'):
                        vn_url = f'https://vndb.org{vn_url}'
                        vn_url_list.append(vn_url)
            vn_url_choice = secrets.choice(vn_url_list)
            async with aiohttp.ClientSession() as session:
                async with session.get(f'{vn_url_choice}/chars') as vn_details_page_session:
                    vn_details_page_html = await vn_details_page_session.text()
            vn_details_page = html.fromstring(vn_details_page_html)
            vn_title = vn_details_page.cssselect('.stripe')[0][0][1].text_content().strip()
            vn_image = vn_details_page.cssselect('.vnimg')[0][0].attrib['src']
            character_objects = vn_details_page.cssselect('.chardetails')[:8]
            character = secrets.choice(character_objects)
            char_img = character[0][0].attrib['src']
            char_name = character[1][0][0][0][0].text.strip()
            await working_response.delete()
            question_embed = discord.Embed(color=0x225588)
            question_embed.set_image(url=char_img)
            question_embed.set_footer(text='You have 30 seconds to guess it.')
            question_embed.set_author(name=vn_title, icon_url=vn_image, url=char_img)
            kud_reward = None
            name_split = char_name.split()
            for name_piece in name_split:
                if kud_reward is None:
                    kud_reward = len(name_piece)
                else:
                    if kud_reward >= len(name_piece):
                        kud_reward = len(name_piece)
            if hint:
                kud_reward = kud_reward // 2
                scrambled_name = scramble(char_name)
                question_embed.description = f'Name: {scrambled_name}'
            await pld.msg.channel.send(embed=question_embed)

            def check_answer(msg):
                """

                :param msg:
                :type msg:
                :return:
                :rtype:
                """
                if pld.msg.channel.id == msg.channel.id:
                    if msg.content.lower() in char_name.lower().split():
                        correct = True
                    elif msg.content.lower() == char_name.lower():
                        correct = True
                    else:
                        correct = False
                else:
                    correct = False
                return correct

            try:
                answer_message = await cmd.bot.wait_for('message', check=check_answer, timeout=30)
                reward_mult = streaks.get(pld.msg.channel.id) or 0
                kud_reward = int(kud_reward * (1 + (reward_mult * 0.35)))
                await cmd.db.add_resource(answer_message.author.id, 'currency', kud_reward, cmd.name, pld.msg)
                author = answer_message.author.display_name
                currency = cmd.bot.cfg.pref.currency
                streaks.update({pld.msg.channel.id: reward_mult + 1})
                win_title = f'🎉 Correct, {author}, it was {char_name}. You won {kud_reward} {currency}!'
                win_embed = discord.Embed(color=0x77B255, title=win_title)
                await pld.msg.channel.send(embed=win_embed)
            except asyncio.TimeoutError:
                if pld.msg.channel.id in streaks:
                    streaks.pop(pld.msg.channel.id)
                timeout_title = f'🕙 Time\'s up! It was {char_name} from {vn_title}...'
                timeout_embed = discord.Embed(color=0x696969, title=timeout_title)
                await pld.msg.channel.send(embed=timeout_embed)
        except (IndexError, KeyError):
            grab_error = error('I failed to grab a character, try again.')
            await pld.msg.channel.send(embed=grab_error)
        if is_ongoing(cmd.name, pld.msg.channel.id):
            del_ongoing(cmd.name, pld.msg.channel.id)
    else:
        ongoing_error = error('There is already one ongoing.')
        await pld.msg.channel.send(embed=ongoing_error)
