import arrow
import discord


async def afk(cmd: SigmaCommand, message: discord.Message, args: list):
    afk_data = await cmd.db[cmd.db.db_cfg.database]['AwayUsers'].find_one({'UserID': message.author.id})
    if args:
        afk_reason = ' '.join(args)
    else:
        afk_reason = 'No reason stated.'
    in_data = {
        'UserID': message.author.id,
        'Timestamp': arrow.utcnow().timestamp,
        'Reason': afk_reason
    }
    if afk_data:
        title = 'Your status has been updated'
        await cmd.db[cmd.db.db_cfg.database]['AwayUsers'].update_one({'UserID': message.author.id}, {'$set': in_data})
    else:
        title = 'You have been marked as away'
        await cmd.db[cmd.db.db_cfg.database]['AwayUsers'].insert_one(in_data)
    url = None
    for piece in afk_reason.split():
        if piece.startswith('http'):
            suffix = piece.split('.')[-1]
            if suffix in ['gif', 'jpg', 'jpeg', 'png']:
                url = piece
                afk_reason = afk_reason.replace(piece, '')
                break
    if not afk_reason:
        afk_reason = 'See image below.'
    response = discord.Embed(color=0x66CC66)
    response.add_field(name=f'✅ {title}.', value=f'Reason: **{afk_reason}**')
    if url:
        response.set_image(url=url)
    await message.channel.send(embed=response)
