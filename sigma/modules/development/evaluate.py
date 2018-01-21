import inspect

import discord

from sigma.core.mechanics.command import SigmaCommand


async def evaluate(cmd: SigmaCommand, message: discord.Message, args: list):
    if not args:
        status = discord.Embed(color=0xBE1931, title='❗ Nothing Inputted To Process')
    else:
        # noinspection PyBroadException
        try:
            execution = " ".join(args)
            output = eval(execution)
            if inspect.isawaitable(output):
                output = await output
            status = discord.Embed(title='✅ Executed', color=0x77B255)
            status.add_field(name='Results', value=f'\n```\n{output}\n```')
        except Exception as e:
            status = discord.Embed(color=0xBE1931, title='❗ Error')
            status.add_field(name='Execution Failed', value=f'{e}')
    await message.channel.send(None, embed=status)
