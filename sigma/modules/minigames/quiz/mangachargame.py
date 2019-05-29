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


async def mangachargame(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if not is_ongoing(cmd.name, pld.msg.channel.id):
        try:
            set_ongoing(cmd.name, pld.msg.channel.id)
            mal_icon = 'https://myanimelist.cdn-dena.com/img/sp/icon/apple-touch-icon-256.png'
            wait_embed = discord.Embed(color=0x1d439b)
            wait_embed.set_author(name='Hunting for a good specimen...', icon_url=mal_icon)
            working_response = await pld.msg.channel.send(embed=wait_embed)
            if pld.args:
                if pld.args[0].lower() == 'hint':
                    hint = True
                else:
                    hint = False
            else:
                hint = False
            ani_order = secrets.randbelow(3) * 50
            if ani_order:
                ani_top_list_url = f'https://myanimelist.net/topmanga.php?limit={ani_order}'
            else:
                ani_top_list_url = 'https://myanimelist.net/topmanga.php'
            async with aiohttp.ClientSession() as session:
                async with session.get(ani_top_list_url) as ani_top_list_session:
                    ani_top_list_html = await ani_top_list_session.text()
            ani_top_list_data = html.fromstring(ani_top_list_html)
            ani_list_objects = ani_top_list_data.cssselect('.ranking-list')
            ani_choice = secrets.choice(ani_list_objects)
            ani_url = ani_choice[1][0].attrib['href']
            async with aiohttp.ClientSession() as session:
                async with session.get(f'{ani_url}/characters') as ani_page_session:
                    ani_page_html = await ani_page_session.text()
            ani_page_data = html.fromstring(ani_page_html)
            cover_object = ani_page_data.cssselect('.ac')[0]
            anime_cover = cover_object.attrib['src']
            anime_title = cover_object.attrib['alt'].strip()
            character_object_list = ani_page_data.cssselect('.borderClass')
            character_list = []
            for char_obj in character_object_list:
                if 'href' in char_obj[0].attrib:
                    if char_obj[1].text_content().strip() == 'Main':
                        character_list.append(char_obj)
            char_choice = secrets.choice(character_list)
            char_url = char_choice[0].attrib['href']
            async with aiohttp.ClientSession() as session:
                async with session.get(char_url) as char_page_session:
                    char_page_html = await char_page_session.text()
            char_page_data = html.fromstring(char_page_html)
            char_img_obj = char_page_data.cssselect('.borderClass')[0][0][0][0]
            char_img = char_img_obj.attrib['src']
            char_name = ' '.join(char_img_obj.attrib['alt'].strip().split(', '))
            await working_response.delete()
            question_embed = discord.Embed(color=0x1d439b)
            question_embed.set_image(url=char_img)
            question_embed.set_footer(text='You have 30 seconds to guess it.')
            question_embed.set_author(name=anime_title, icon_url=anime_cover, url=char_img)
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
                timeout_title = f'🕙 Time\'s up! It was {char_name} from {anime_title}...'
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
