async def test(cmd: SigmaCommand, message: discord.Message, args: list):
    await message.channel.send('All good!')
