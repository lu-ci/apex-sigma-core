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

import discord
from lxml import html

from sigma.core.utilities.generic_responses import GenericResponse
from sigma.core.utilities.url_processing import aioget
from sigma.modules.minigames.quiz.mech.utils import scramble
from sigma.modules.minigames.utils.ongoing.ongoing import Ongoing
from sigma.modules.searches.vndb.models.visual_novel import VisualNovel

streaks = {}


async def vnchargame(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if not Ongoing.is_ongoing(cmd.name, pld.msg.channel.id):
        try:
            Ongoing.set_ongoing(cmd.name, pld.msg.channel.id)
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
            vn_top_list_url = 'https://vndb.org/v/all?q=;fil=tagspoil-0;rfil=;o=d;s=pop;p=1'
            vn_top_list_html = await aioget(vn_top_list_url)
            vn_top_list_data = html.fromstring(vn_top_list_html)
            cards = vn_top_list_data.cssselect('.vncards')[0]
            for card in cards:
                entry = card[1]
                vn_url = entry[0].attrib['href']
                vn_url = f'https://vndb.org{vn_url}'
                vn_url_list.append(vn_url)
            vn_url_choice = secrets.choice(vn_url_list)
            vn_details_page_html = await aioget(f'{vn_url_choice}/chars')
            vn_details_page = html.fromstring(vn_details_page_html)
            details = vn_details_page.cssselect('.vndetails')[0]
            detail_table = details[1]
            vn_title = VisualNovel.title_from_details(detail_table)
            vn_image = vn_details_page.cssselect('.vnimg')[0][0][0][0].attrib['src']
            character_objects = vn_details_page.cssselect('.chardetails')[:8]
            character = secrets.choice(character_objects)
            char_img = character[0][0][0][0].attrib['src']
            char_name = character[1][0][0][0][0].text.strip()

            kud_reward = None
            description = None
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
                description = f'Name: {scrambled_name}'
            reward_mult = streaks.get(pld.msg.channel.id) or 0
            kud_reward = int(kud_reward * (1 + (reward_mult * 2.25) / (1.75 + (0.03 * reward_mult))))

            try:
                await working_response.delete()
            except discord.NotFound:
                pass
            question_embed = discord.Embed(color=0x225588)
            if description:
                question_embed.description = description
            question_embed.set_image(url=char_img)
            question_embed.set_thumbnail(url=vn_image)
            question_embed.set_author(name=vn_title, icon_url=vndb_icon, url=char_img)
            footer_text = 'You have 30 seconds to guess it.'
            if reward_mult:
                footer_text += f' | Streak: {int(reward_mult)}'
            question_embed.set_footer(text=footer_text)
            await pld.msg.channel.send(embed=question_embed)

            def check_answer(msg):
                """
                :type msg: discord.Message
                :rtype: bool
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
        except (SyntaxError):
            grab_error = GenericResponse('I failed to grab a character, try again.').error()
            await pld.msg.channel.send(embed=grab_error)
        if Ongoing.is_ongoing(cmd.name, pld.msg.channel.id):
            Ongoing.del_ongoing(cmd.name, pld.msg.channel.id)
    else:
        ongoing_error = GenericResponse('There is already one ongoing.').error()
        await pld.msg.channel.send(embed=ongoing_error)
