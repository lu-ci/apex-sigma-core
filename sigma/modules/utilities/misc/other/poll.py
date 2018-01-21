from sigma.core.mechanics.command import SigmaCommand
import secrets

import discord


async def poll(cmd: SigmaCommand, message: discord.Message, args: list):
    if not args:
        out_content = discord.Embed(type='rich', color=0xBE1931,
                                    title='❗ Missing Arguments.')
        await message.channel.send(None, embed=out_content)
        return
    all_qry = ' '.join(args)
    if all_qry.endswith(';'):
        all_qry = all_qry[:-1]
    poll_name = all_qry.split('; ')[0]
    choice_qry = '; '.join(all_qry.split('; ')[1:])
    if choice_qry.endswith(';'):
        choice_qry = choice_qry[:-1]
    poll_choices = choice_qry.split('; ')
    if len(poll_choices) < 2:
        out_content = discord.Embed(type='rich', color=0xBE1931,
                                    title='❗ Not enough arguments present.')
        await message.channel.send(None, embed=out_content)
        return
    if len(poll_choices) > 9:
        out_content = discord.Embed(type='rich', color=0xBE1931,
                                    title='❗ Maximum is 9 choices.')
        await message.channel.send(None, embed=out_content)
        return
    icon_list_base = ['🍏', '🍍', '🍐', '🌶', '🍆', '🍋', '🍌', '🍅', '🍓', '🍇']
    choice_text = ''
    op_num = 0
    emoji_list = []
    for option in poll_choices:
        emoji = icon_list_base.pop(secrets.randbelow(len(icon_list_base)))
        emoji_list.append(emoji)
        choice_text += '\n' + emoji + ' - **' + option + '**'
        op_num += 1
    out_content = discord.Embed(color=0x1ABC9C)
    out_content.add_field(name=poll_name, value=choice_text)
    poll_message = await message.channel.send(None, embed=out_content)
    ic_num = 0
    for emoji in emoji_list:
        await poll_message.add_reaction(emoji=emoji)
        ic_num += 1
