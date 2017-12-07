import arrow

from sigma.modules.core_functions.stats.stats_temp_storage import StatisticsStorage

stats_handler = None


async def add_cmd_stat(db, cmd, message, args):
    if not message.author.bot:
        if message.guild:
            channel_id = message.channel.id
            guild_id = message.guild.id
        else:
            channel_id = None
            guild_id = None
        stat_data = {
            'command': cmd.name,
            'args': args,
            'author': message.author.id,
            'channel': channel_id,
            'guild': guild_id,
            'timestamp': {
                'created': arrow.get(message.created_at).float_timestamp,
                'executed': arrow.utcnow().float_timestamp
            }
        }
        await db[db.db_cfg.database]['CommandStats'].insert_one(stat_data)


async def add_special_stats(db, stat_name):
    global stats_handler
    if not stats_handler:
        stats_handler = StatisticsStorage(db, stat_name)
    stats_handler.add_stat()
