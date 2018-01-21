from sigma.core.mechanics.command import SigmaCommand
import discord


async def removestatus(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        status_id = ''.join(args)
        status_data = {'ID': status_id}
        status_exists = await cmd.db[cmd.db.db_cfg.database].StatusFiles.find_one(status_data)
        if status_exists:
            await cmd.db[cmd.db.db_cfg.database].StatusFiles.delete_one(status_data)
            response = discord.Embed(color=0x77B255, title=f'✅ Deleted status `{status_id}`.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Status ID not found.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputed.')
    await message.channel.send(embed=response)
