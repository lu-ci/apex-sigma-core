import arrow
import discord


async def afk(cmd, message, args):
    afk_data = cmd.db[cmd.db.db_cfg.database]['AwayUsers'].find_one({'UserID': message.author.id})
    if afk_data:
        response = discord.Embed(color=0xBE1931, title='❗ You are already marked as AFK.')
    else:
        if args:
            afk_reason = ' '.join(args)
        else:
            afk_reason = 'No reason stated.'
        in_data = {
            'UserID': message.author.id,
            'Timestamp': arrow.utcnow().timestamp,
            'Reason': afk_reason
        }
        cmd.db[cmd.db.db_cfg.database]['AwayUsers'].insert_one(in_data)
        url = None
        for piece in afk_reason.split():
            if piece.startswith('http'):
                suffix = piece.split('.')[-1]
                if suffix in ['gif', 'jpg', 'jpeg', 'png']:
                    url = piece
                    afk_reason = afk_reason.replace(piece, '')
                    break
        response = discord.Embed(color=0x66CC66)
        response.add_field(name='✅ You have been marked as afk.', value=f'Reason: **{afk_reason}**')
        if url:
            response.set_image(url=url)
    await message.channel.send(embed=response)
