import discord
from sigma.core.mechanics.command import SigmaCommand

from .nodes.item_core import ItemCore

item_core = None


async def finditem(cmd: SigmaCommand, message: discord.Message, args: list):
    global item_core
    if not item_core:
        item_core = ItemCore(cmd.resource('data'))
    if args:
        lookup = ' '.join(args)
        item = item_core.get_item_by_name(lookup)
        if item:
            response = item.make_inspect_embed(cmd.bot.cfg.pref.currency)
        else:
            response = discord.Embed(color=0x696969, title=f'🔍 I didn\'t find any {lookup}.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ You didn\'t input anything.')
    await message.channel.send(embed=response)
