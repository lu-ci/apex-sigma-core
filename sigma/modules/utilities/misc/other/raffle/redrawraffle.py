async def redrawraffle(cmd, message, args):
    if args:
        rafid = args[0].lower()
        raffle = await cmd.db[cmd.db.db_cfg.database].Raffles.find_one({'ID': rafid, 'Active': False})
        if raffle:
            aid = raffle.get('Author')
            if aid == message.author.id:
                await cmd.db[cmd.db.db_cfg.database].Raffles.update_one(raffle, {'$set': {'Active': True}})
                reaction = '✅'
            else:
                reaction = '⛔'
        else:
            reaction = '🔍'
    else:
        reaction = '❗'
    await message.add_reaction(reaction)
