import discord

from sigma.core.mechanics.command import SigmaCommand


async def test(cmd: SigmaCommand, message: discord.Message, args: list):
    await message.channel.send('All good!')
