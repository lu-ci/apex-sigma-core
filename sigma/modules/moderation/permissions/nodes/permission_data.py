def generate_default_data(message):
    perm_data = {
        'ServerID': message.guild.id,
        'DisabledCommands': [],
        'DisabledModules': [],
        'CommandExceptions': {},
        'ModuleExceptions': {},
    }
    return perm_data


def generate_cmd_data(cmd_name):
    generic_data = {
        'Users': [],
        'Channels': [],
        'Roles': []
    }
    return {cmd_name: generic_data}


async def get_all_perms(db, message):
    perms = await db[db.db_cfg.database].Permissions.find_one({'ServerID': message.guild.id})
    if not perms:
        perms = generate_default_data(message)
        await db[db.db_cfg.database].Permissions.insert_one(perms)
    return perms
