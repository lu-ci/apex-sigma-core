import arrow
import discord
from sigma.core.mechanics.command import SigmaCommand

emote_cache = {'stamp': 0, 'emotes': []}


def emote_filler(guilds):
    emote_list = []
    for guild in guilds:
        if guild.emojis:
            for emoji in guild.emojis:
                emote_list.append(emoji)
    return emote_list


async def emote(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        lookup = args[0].lower()
        if ':' in lookup:
            split_args = lookup.split(':')
            lookup = split_args[0]
            try:
                eid = int(split_args[1])
            except ValueError:
                eid = None
        else:
            eid = None
        if arrow.utcnow().timestamp > emote_cache.get('stamp') + 300:
            all_emotes = emote_filler(cmd.bot.guilds)
            emote_cache.update({'stamp': arrow.utcnow().timestamp, 'emotes': all_emotes})
        else:
            all_emotes = emote_cache.get('emotes')
        if eid:
            emote_choice = discord.utils.find(lambda x: x.name.lower() == lookup and x.id == eid, all_emotes)
            if not emote_choice:
                emote_choice = discord.utils.find(lambda x: x.name.lower() == lookup and x.guild.id == eid, all_emotes)
        else:
            sid = message.guild.id
            emote_priority = discord.utils.find(lambda x: x.name.lower() == lookup and x.guild.id == sid, all_emotes)
            if emote_priority:
                emote_choice = emote_priority
            else:
                emote_choice = discord.utils.find(lambda x: x.name.lower() == lookup, all_emotes)
        if emote_choice:
            response = discord.Embed().set_image(url=emote_choice.url)
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Emote not found.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
