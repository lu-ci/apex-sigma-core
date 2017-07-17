import re
import arrow
import aiohttp


def user_avatar(user):
    if user.avatar_url:
        output = user.avatar_url
    else:
        output = user.default_avatar_url
    return output


def movement_message_parser(member, text):
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


def get_time_difference(member, leave=False):
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
    url_base = "https://www.youtube.com/results?"
    params = {
        "q": qry
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{url_base}', params=params) as data:
            html_content = await data.text()
            search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content)
            video_url = f'https://www.youtube.com/watch?v={search_results[0]}'
    return video_url
