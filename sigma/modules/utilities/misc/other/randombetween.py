import secrets

import discord

from sigma.core.mechanics.command import SigmaCommand


async def randombetween(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        if len(args) == 2:
            try:
                min_num = int(args[0])
                max_num = int(args[1])
            except ValueError:
                min_num = None
                max_num = None
            if min_num and max_num:
                if max_num > min_num:
                    ran_num = secrets.randbelow(max_num - min_num)
                    out_num = min_num + ran_num
                    response = discord.Embed(color=0xea596e, title=f'🎲 {out_num}')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ The high number is smaller than the minimum.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Invalid numbers.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Invalid number of arguments.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
