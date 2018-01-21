import discord

from sigma.modules.minigames.professions.nodes.item_core import ItemCore

item_core = None


async def generateitem(cmd: SigmaCommand, message: discord.Message, args: list):
    global item_core
    if not item_core:
        item_core = ItemCore('sigma/modules/minigames/professions/res/data')
    if args:
        if message.mentions:
            if len(args) >= 3:
                target = message.mentions[0]
                lookup = ' '.join(args[1:])
                item = item_core.get_item_by_name(lookup)
                if item:
                    connector = 'a'
                    if item.name[0].lower() in ['a', 'e', 'i', 'o', 'u']:
                        connector = 'an'
                    data_for_inv = item.generate_inventory_item()
                    await cmd.db.add_to_inventory(target, data_for_inv)
                    success_text = f'{item.icon} I have given {connector} {item.name} to {target.display_name}.'
                    response = discord.Embed(color=item.color, title=success_text)
                else:
                    response = discord.Embed(color=0x696969, title=f'🔍 I didn\'t find any {lookup}.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Not enough arguments.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ No user targeted.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ You didn\'t input anything.')
    await message.channel.send(embed=response)
