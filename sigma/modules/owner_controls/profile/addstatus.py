import secrets

import discord


async def addstatus(cmd, message, args):
    if args:
        status_text = ' '.join(args)
        status_exists = await cmd.db[cmd.db.db_cfg.database].StatusFiles.find_one({'Text': status_text})
        if not status_exists:
            status_id = secrets.token_hex(5)
            status_data = {
                'Text': status_text,
                'ID': status_id
            }
            await cmd.db[cmd.db.db_cfg.database].StatusFiles.insert_one(status_data)
            response = discord.Embed(color=0x77B255, title=f'✅ Added status `{status_id}`.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Status already exists.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputed.')
    await message.channel.send(embed=response)
