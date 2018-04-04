# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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

import io
import re

import aiohttp
import arrow
import discord
from PIL import Image

color_cache = {}


def convert_to_seconds(time_input: str):
    indent_list = time_input.split(':')
    if len(indent_list) == 3:
        output = (3600 * int(indent_list[0])) + (60 * int(indent_list[1]) + int(indent_list[2]))
    elif len(indent_list) == 2:
        output = (60 * int(indent_list[0]) + int(indent_list[1]))
    elif len(indent_list) == 1:
        output = int(indent_list[0])
    else:
        raise LookupError
    return output


def user_avatar(user: discord.Member, gif: bool = False, static: bool = False):
    if user.avatar_url:
        output = user.avatar_url
    else:
        output = user.default_avatar_url
    if gif:
        output = f"{'.'.join(output.split('.')[:-1])}.gif"
    else:
        if user.avatar:
            if user.avatar.startswith('a_') and not static:
                output = f"{'.'.join(output.split('.')[:-1])}.gif"
            else:
                output = f"{'.'.join(output.split('.')[:-1])}.png?size=1024"
        else:
            output = user.default_avatar_url
    return output


def command_message_parser(message: discord.Message, text: str):
    gld = message.guild
    ath = message.author
    chn = message.channel
    command_text = text
    if message.mentions:
        tgt = message.mentions[0]
    else:
        tgt = ath
    translator = {
        '{author_name}': ath.name,
        '{author_nick}': ath.display_name,
        '{author_mention}': ath.mention,
        '{author_id}': str(ath.id),
        '{channel_name}': chn.name,
        '{channel_mention}': chn.mention,
        '{channel_id}': str(chn.id),
        '{server_name}': gld.name,
        '{server_id}': str(gld.id),
        '{target_name}': tgt.name,
        '{target_nick}': tgt.display_name,
        '{target_mention}': tgt.mention,
        '{target_id}': str(tgt.id)
    }
    for key in translator:
        command_text = command_text.replace(key, translator[key])
    return command_text


def movement_message_parser(member: discord.Member, text: str):
    guild = member.guild
    translator = {
        '{user_name}': member.name,
        '{user_mention}': member.mention,
        '{user_discriminator}': member.discriminator,
        '{user_id}': str(member.id),
        '{server_name}': guild.name,
        '{server_id}': str(guild.id),
        '{owner_name}': guild.owner.name,
        '{owner_mention}': guild.owner.mention,
        '{owner_discriminator}': guild.owner.discriminator,
        '{owner_id}': str(guild.owner.id)
    }
    greeting_text = text
    for key in translator:
        greeting_text = greeting_text.replace(key, translator[key])
    return greeting_text


def get_time_difference(member: discord.Member, leave: bool = False):
    if leave:
        creation_time = member.joined_at
    else:
        creation_time = member.created_at
    creation_time = arrow.get(creation_time)
    creation_timestamp = creation_time.timestamp
    current_timestamp = arrow.utcnow().timestamp
    if current_timestamp - creation_timestamp < 600:
        new_acc = True
    else:
        new_acc = False
    human_msg = creation_time.humanize(arrow.utcnow())
    return new_acc, human_msg


async def search_youtube(qry: str):
    url_base = "https://www.youtube.com/results?"
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{url_base}', params={"q": qry}) as data:
            html_content = await data.text()
            search_results = re.findall(r'href=\"/watch\?v=(.{11})', html_content)
            video_url = f'https://www.youtube.com/watch?v={search_results[0]}'
    return video_url


def rgb_maximum(colors_tuple: list):
    r_sorted_tuple = sorted(colors_tuple, key=lambda x: x[1][0])
    g_sorted_tuple = sorted(colors_tuple, key=lambda x: x[1][1])
    b_sorted_tuple = sorted(colors_tuple, key=lambda x: x[1][2])

    r_min = r_sorted_tuple[0][1][0]
    g_min = g_sorted_tuple[0][1][1]
    b_min = b_sorted_tuple[0][1][2]

    r_max = r_sorted_tuple[len(colors_tuple) - 1][1][0]
    g_max = g_sorted_tuple[len(colors_tuple) - 1][1][1]
    b_max = b_sorted_tuple[len(colors_tuple) - 1][1][2]

    return {
        "r_max": r_max,
        "r_min": r_min,
        "g_max": g_max,
        "g_min": g_min,
        "b_max": b_max,
        "b_min": b_min,
        "r_dvalue": (r_max - r_min) / 3,
        "g_dvalue": (g_max - g_min) / 3,
        "b_dvalue": (b_max - b_min) / 3
    }


def group_by_accuracy(sorted_tuple: list):
    rgb_maximum_json = rgb_maximum(sorted_tuple)
    r_min = rgb_maximum_json["r_min"]
    g_min = rgb_maximum_json["g_min"]
    b_min = rgb_maximum_json["b_min"]
    r_dvalue = rgb_maximum_json["r_dvalue"]
    g_dvalue = rgb_maximum_json["g_dvalue"]
    b_dvalue = rgb_maximum_json["b_dvalue"]

    rgb = [
        [[[], [], []], [[], [], []], [[], [], []]],
        [[[], [], []], [[], [], []], [[], [], []]],
        [[[], [], []], [[], [], []], [[], [], []]]
    ]

    for color_tuple in sorted_tuple:
        r_tmp_i = color_tuple[1][0]
        g_tmp_i = color_tuple[1][1]
        b_tmp_i = color_tuple[1][2]
        r_idx = 0 if r_tmp_i < (r_min + r_dvalue) else 1 if r_tmp_i < (r_min + r_dvalue * 2) else 2
        g_idx = 0 if g_tmp_i < (g_min + g_dvalue) else 1 if g_tmp_i < (g_min + g_dvalue * 2) else 2
        b_idx = 0 if b_tmp_i < (b_min + b_dvalue) else 1 if b_tmp_i < (b_min + b_dvalue * 2) else 2
        rgb[r_idx][g_idx][b_idx].append(color_tuple)
    return rgb


def get_weighted_mean(grouped_image_color: list):
    sigma_count = 0
    sigma_r = 0
    sigma_g = 0
    sigma_b = 0

    for item in grouped_image_color:
        sigma_count += item[0]
        sigma_r += item[1][0] * item[0]
        sigma_g += item[1][1] * item[0]
        sigma_b += item[1][2] * item[0]

    r_weighted_mean = int(sigma_r / sigma_count)
    g_weighted_mean = int(sigma_g / sigma_count)
    b_weighted_mean = int(sigma_b / sigma_count)

    weighted_mean = (sigma_count, (r_weighted_mean, g_weighted_mean, b_weighted_mean))
    return weighted_mean


def rgb_to_hex(rgb_tuple: tuple):
    hex_str = ''
    for piece in rgb_tuple:
        hex_piece = str(hex(piece))
        hex_piece = hex_piece.split('x')[1]
        if len(hex_piece) == 1:
            hex_piece = '0' + hex_piece
        hex_str += hex_piece
    hex_out = int(f'0x{hex_str}', 16)
    return hex_out


async def get_image_colors(img_url: str):
    if img_url:
        cached_color = color_cache.get(img_url)
        if not cached_color:
            async with aiohttp.ClientSession() as session:
                async with session.get(img_url) as img_session:
                    img_data = await img_session.read()
                    img_data = io.BytesIO(img_data)
            with Image.open(img_data) as img:
                img = img.convert('RGBA')
                img_h = img.height
                img_w = img.width
                color_count = img_h * img_w
                colors = img.getcolors(color_count)
                sorted_by_rgb = sorted(colors, key=lambda x: x[1])
                grouped_colors = group_by_accuracy(sorted_by_rgb)
                mean = []
                for i in range(3):
                    for j in range(3):
                        for k in range(3):
                            grouped_image_color = grouped_colors[i][j][k]
                            if 0 != len(grouped_image_color):
                                color_mean = get_weighted_mean(grouped_image_color)
                                mean.append(color_mean)
                mean = sorted(mean, reverse=True)
            dominant = mean[0][1]
            color_cache.update({img_url: dominant})
        else:
            dominant = cached_color
    else:
        dominant = (105, 105, 105)
    dominant = rgb_to_hex(dominant)
    return dominant
