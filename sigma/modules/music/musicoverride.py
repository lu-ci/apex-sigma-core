# noinspection PyBroadException,PyBroadException,PyBroadException,PyBroadException
async def musicoverride(cmd, message, args):
    if message.guild.me.voice:
        try:
            await message.guild.me.voice.channel.connect()
        except Exception:
            pass
    if message.guild.voice_client:
        try:
            await message.guild.voice_client.disconnect()
        except Exception:
            pass
    if message.author.voice:
        try:
            await message.author.voice.channel.connect()
        except Exception:
            pass
    if message.guild.voice_client:
        try:
            await message.guild.voice_client.disconnect()
        except Exception:
            pass
