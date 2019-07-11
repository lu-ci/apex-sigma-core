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

import io
import re

import aiohttp
import arrow
import discord
from PIL import Image

color_cache_coll = None


def set_color_cache_coll(coll):
    """
    Sets the color cache to the given database collection.
    :param coll: The database collection to set as the cache.
    :type coll: motor.motor_asyncio.AsyncIOMotorCollection
    """
    global color_cache_coll
    color_cache_coll = coll


def convert_to_seconds(time_input):
    """
    Converts time with the format H:M:S into seconds.
    :param time_input: The time to covert into seconds.
    :type time_input: str
    :return:
    :rtype: int
    """
    indent_list = time_input.split(':')
    try:
        if len(indent_list) == 3:
            output = (3600 * int(indent_list[0])) + (60 * int(indent_list[1]) + int(indent_list[2]))
        elif len(indent_list) == 2:
            output = (60 * int(indent_list[0]) + int(indent_list[1]))
        elif len(indent_list) == 1:
            output = int(indent_list[0])
        else:
            raise LookupError
    except ValueError:
        raise LookupError
    return output


def user_avatar(user, gif=False, static=False):
    """
    Fetches the avatar of Discord member.
    :param user: The user to fetch the avatar from.
    :type user: discord.Member
    :param gif: Whether or not the returned image should be a GIF.
    :type gif: bool
    :param static: Whether or not the returned image should be static.
    :type static: bool
    :return:
    :rtype: str
    """
    if user.avatar_url:
        output = user.avatar_url
    else:
        output = user.default_avatar_url
    output = str(output)
    if gif:
        output = f"{'.'.join(output.split('.')[:-1])}.gif"
    else:
        if user.avatar_url:
            if str(user.avatar).startswith('a_') and not static:
                output = f"{'.'.join(output.split('.')[:-1])}.gif"
            else:
                output = f"{'.'.join(output.split('.')[:-1])}.png?size=1024"
        else:
            output = str(user.default_avatar_url)
    return output


def command_message_parser(message, text):
    """
    Parses variables in the output of custom commands.
    :param message: The message object to fill in variables.
    :type message: discord.Message
    :param text: The text output of the custom command.
    :type text: str
    :return:
    :rtype: str
    """
    gld = message.guild
    ath = message.author
    chn = message.channel
    command_text = text
    tgt = message.mentions[0] if message.mentions else ath
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
        '{target_id}': str(tgt.id),
        '{population}': str(len(gld.members))
    }
    for key in translator:
        command_text = command_text.replace(key, translator[key])
    return command_text


def movement_message_parser(member, text):
    """
    Parses variables in the output of movement messages.
    :param member: The member object to fill in variables.
    :type member: discord.Member
    :param text: The text output of the movement message.
    :type text: str
    :return:
    :rtype: str
    """
    guild = member.guild
    greeting_text = text
    translator = {
        '{user_name}': member.name,
        '{user_nick}': member.display_name,
        '{user_mention}': member.mention,
        '{user_discriminator}': member.discriminator,
        '{user_id}': str(member.id),
        '{server_name}': guild.name,
        '{server_id}': str(guild.id),
        '{owner_name}': guild.owner.name,
        '{owner_nick}': guild.owner.display_name,
        '{owner_mention}': guild.owner.mention,
        '{owner_discriminator}': guild.owner.discriminator,
        '{owner_id}': str(guild.owner.id),
        '{population}': str(len(guild.members))
    }
    for key in translator:
        greeting_text = greeting_text.replace(key, translator[key])
    return greeting_text


def get_time_difference(member, leave=False):
    """
    Gets the difference between a member's creation or join date and the current UTC time.
    :param member: The member object to fetch from.
    :type member: discord.Member
    :param leave: Whether to fetch the creation date or guild join date.
    :type leave: bool
    :return:
    :rtype: (bool, str)
    """
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


async def search_youtube(qry):
    """
    Searches youtube with the given query.
    :param qry: The query to search for.
    :type qry: str
    :return:
    :rtype: str
    """
    url_base = "https://www.youtube.com/results?"
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{url_base}', params={"q": qry}) as data:
            html_content = await data.text()
            # matches video hyperlinks in YouTube's results HTML
            search_results = re.findall(r'href=\"/watch\?v=(.{11})', html_content)
            video_url = f'https://www.youtube.com/watch?v={search_results[0]}'
    return video_url


def rgb_maximum(colors_tuple):
    """
    :param colors_tuple: Tuple of RGB color values.
    :type colors_tuple: list[tuple]
    :return:
    :rtype: dict
    """
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


def group_by_accuracy(sorted_tuple):
    """
    :param sorted_tuple: List of sorted RGB color values.
    :type sorted_tuple: list[tuple]
    :return:
    :rtype: list[tuple]
    """
    rgb_maximum_json = rgb_maximum(sorted_tuple)
    r_min = rgb_maximum_json.get("r_min")
    g_min = rgb_maximum_json.get("g_min")
    b_min = rgb_maximum_json.get("b_min")
    r_dvalue = rgb_maximum_json.get("r_dvalue")
    g_dvalue = rgb_maximum_json.get("g_dvalue")
    b_dvalue = rgb_maximum_json.get("b_dvalue")

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


def get_weighted_mean(grouped_image_color):
    """
    :param grouped_image_color: List of colors in RGB groups.
    :type grouped_image_color: list[tuple]
    :return:
    :rtype:
    """
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


def rgb_to_hex(rgb_tuple):
    """
    Converts an RGB tuple into a decimal color.
    :param rgb_tuple: The RGB tuple to convert.
    :type rgb_tuple: tuple
    :return:
    :rtype: int
    """
    hex_str = ''
    for piece in rgb_tuple:
        hex_piece = str(hex(piece))
        hex_piece = hex_piece.split('x')[1]
        if len(hex_piece) == 1:
            hex_piece = '0' + hex_piece
        hex_str += hex_piece
    hex_out = int(f'0x{hex_str}', 16)
    return hex_out


async def get_image_colors(img_url):
    """
    Fetches the most dominant color from an image.
    :param img_url: The image to fetch from.
    :type img_url: str
    :return:
    :rtype: int
    """
    if img_url:
        img_url = str(img_url)
        cached_color = await color_cache_coll.find_one({'url': img_url})
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
            await color_cache_coll.insert_one({'url': img_url, 'color': dominant})
        else:
            dominant = cached_color.get('color')
    else:
        dominant = (105, 105, 105)
    dominant = rgb_to_hex(dominant)
    return dominant


def get_broad_target(pld):
    """
    Gets a target from a message by mentions, ID and name, nickname.
    :param pld: The command payload to process.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    :return:
    :rtype: discord.Member or None
    """
    target = None
    if pld.msg.mentions:
        target = pld.msg.mentions[0]
    else:
        if pld.args:
            try:
                possible_id = int(pld.args[0])
            except ValueError:
                possible_id = None
            if possible_id is not None:
                target = pld.msg.guild.get_member(possible_id)
            else:
                possible_name = ' '.join(pld.args)
                for member in pld.msg.guild.members:
                    name_match = member.name.lower() == possible_name.lower()
                    display_name_match = member.display_name.lower() == possible_name.lower()
                    if name_match or display_name_match:
                        target = member
                        break
    return target
